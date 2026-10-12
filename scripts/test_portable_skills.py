#!/usr/bin/env python3
"""Regression coverage for derived versions and complete portable exports."""
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import package_skill
sync = package_skill.sync


class PortableSkillsTest(unittest.TestCase):
    def test_version_sources(self):
        for declaration, expected in [
            ('metadata:\n  version: "1.2"', '1.2.0'),
            ("version: '2.3.4'", '2.3.4'),
            ('metadata:\n  version: "1.0.4-rc1"', '1.0.4-rc1'),
            ('name: sample', None),
        ]:
            self.assertEqual(sync.declared_version('---\n' + declaration + '\n---\n'), expected)

    def test_sync_preserves_registry_only_fields_and_converges(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / 'skills/demo/sample'
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').write_text('---\nname: sample\ndescription: Demo\nmetadata:\n  version: "2.1"\n---\n# Demo\n')
            registry_path = root / 'registry.json'
            registry_path.write_text(json.dumps({'skills': {'sample': {
                'location': 'skills/demo/sample/SKILL.md', 'version': '1.0.0',
                'manual_notes': 'retain me', 'type': 'action', 'depends_on': []}}}))
            with patch.object(sync, 'PROJECT_ROOT', root), patch.object(sync, 'SKILLS_DIR', root / 'skills'), patch.object(sync, 'REGISTRY_PATH', registry_path), patch.object(sync, '_tracked_files', return_value=frozenset()), contextlib.redirect_stdout(io.StringIO()):
                sync.sync(apply=True)
                result = json.loads(registry_path.read_text())['skills']['sample']
                self.assertEqual(result['version'], '2.1.0')
                self.assertEqual(result['manual_notes'], 'retain me')
                self.assertEqual(result['type'], 'action')
                capture = io.StringIO()
                with contextlib.redirect_stdout(capture):
                    sync.sync()
                self.assertIn('Registry is in sync.', capture.getvalue())
                (skill / 'SKILL.md').unlink()
                capture = io.StringIO()
                with contextlib.redirect_stdout(capture):
                    sync.sync()
                self.assertNotIn('Registry is in sync.', capture.getvalue())

    def test_metadata_change_during_export_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'sample'
            source.mkdir()
            (source / 'SKILL.md').write_text('---\nname: sample\nversion: 1.0\n---\n')
            original_copy = package_skill.shutil.copy2
            def mutate_then_copy(path, target):
                if path.name == 'SKILL.md':
                    path.write_text(path.read_text().replace('1.0', '2.0'))
                return original_copy(path, target)
            with patch.object(package_skill.shutil, 'copy2', mutate_then_copy):
                with self.assertRaisesRegex(ValueError, 'metadata changed'):
                    package_skill.package(source, root / 'exports', root)
            self.assertFalse((root / 'exports/sample-export').exists())

    def test_complete_export_and_safe_rerun(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'skills/demo/sample'
            source.mkdir(parents=True)
            (source / 'SKILL.md').write_text('---\nname: sample\nmetadata:\n  version: "2.1"\n---\n# Demo\n')
            for filename in ['agents/nested/a.md', 'scripts/run.py', 'assets/image.bin', 'references/r.json', 'templates/t.txt', 'eval/case.json', 'README.md']:
                file = source / filename
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(b'original\x00\xff')
            (root / 'data').mkdir()
            (root / 'data/registry.json').write_text(json.dumps({'skills': {'sample': {'location': 'skills/demo/sample/SKILL.md', 'type': 'orchestrator', 'depends_on': ['missing']}}}))
            with patch.object(sync, '_tracked_files', return_value=frozenset()):
                result = package_skill.package(source, root / 'exports', root)
                bundle = Path(result['export_dir'])
                manifest = json.loads((bundle / 'manifest.json').read_text())
                self.assertEqual(manifest['skill']['version'], '2.1.0')
                self.assertEqual(manifest['skill']['type'], 'orchestrator')
                self.assertEqual(manifest['dependencies']['unknown_skills'], ['missing'])
                self.assertFalse(manifest['self_contained'])
                for relative, digest in manifest['files'].items():
                    self.assertEqual((source / relative).read_bytes(), (bundle / relative).read_bytes())
                    self.assertEqual(package_skill.hashlib.sha256((bundle / relative).read_bytes()).hexdigest(), digest)
                original_rename = Path.rename
                # Fail once so rollback itself can still rename the backup.
                failed = False
                def fail_once(path, target):
                    nonlocal failed
                    if not failed and path != bundle and (path / 'manifest.json').is_file():
                        failed = True
                        raise OSError('simulated promotion failure')
                    return original_rename(path, target)
                with patch.object(Path, 'rename', fail_once):
                    with self.assertRaisesRegex(OSError, 'promotion'):
                        package_skill.package(source, root / 'exports', root)
                self.assertEqual(json.loads((bundle / 'manifest.json').read_text()), manifest)
                (source / 'templates/t.txt').unlink()
                package_skill.package(source, root / 'exports', root)
                self.assertFalse((bundle / 'templates/t.txt').exists())
                external = root / 'external/sample'
                external.mkdir(parents=True)
                (external / 'SKILL.md').write_text((source / 'SKILL.md').read_text())
                external_result = package_skill.package(external, root / 'external-exports', root)
                external_manifest = json.loads((Path(external_result['export_dir']) / 'manifest.json').read_text())
                self.assertEqual(external_manifest['dependencies']['depends_on'], [])
                self.assertTrue(any('not registered' in w for w in external_manifest['warnings']))
                (source / 'assets/link').symlink_to(root / 'data/registry.json')
                with self.assertRaisesRegex(ValueError, 'Symlink'):
                    package_skill.package(source, root / 'exports', root)
                self.assertTrue((bundle / 'SKILL.md').exists())
                with self.assertRaisesRegex(ValueError, 'outside'):
                    package_skill.package(source, source / 'exports', root)


if __name__ == '__main__':
    unittest.main()
