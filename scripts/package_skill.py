#!/usr/bin/env python3
"""Build a portable, byte-verifiable skill snapshot using existing metadata."""
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("registry_sync", ROOT / "scripts/sync-registry.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


def package(source: Path, output: Path, root: Path = ROOT) -> dict:
    source, output, root = source.resolve(), output.resolve(), root.resolve()
    if not (source / "SKILL.md").is_file():
        raise ValueError(f"SKILL.md not found: {source}")
    if output == source or output.is_relative_to(source):
        raise ValueError("Output must be outside the source skill directory")
    text = (source / "SKILL.md").read_text()
    metadata = sync.extract_yaml_frontmatter(text) or {}
    name = metadata.get("name", source.name).strip("\"'")
    if not name or Path(name).name != name or name in {".", ".."}:
        raise ValueError("Invalid skill name")
    registry_path = root / "data/registry.json"
    registry = json.loads(registry_path.read_text()) if registry_path.exists() else {}
    entry = registry.get("skills", {}).get(name, {})
    # A matching name alone cannot establish provenance for an external skill.
    if entry and (root / entry.get("location", "")).resolve() != source / "SKILL.md":
        entry = {}

    version = sync.declared_version(text) or entry.get("version", "unknown")
    dependencies = entry.get("depends_on", [])
    files = []
    for path in sorted(source.rglob("*")):
        rel = path.relative_to(source)
        if any(part.startswith(".") or part == "__pycache__" for part in rel.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Symlink must be resolved before export: {rel}")
        if path.is_file():
            files.append((path, rel))
    # Metadata files must never overwrite authored supporting content.
    if any(rel.as_posix() == "manifest.json" for _, rel in files):
        raise ValueError("Authored manifest.json conflicts with generated export metadata")
    try:
        revision = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = bool(subprocess.check_output(["git", "-C", str(root), "status", "--porcelain", "--", str(source), str(registry_path)], text=True))
    except (OSError, subprocess.CalledProcessError):
        revision, dirty = None, None
    output.mkdir(parents=True, exist_ok=True)
    destination = output / f"{name}-export"
    if destination == source or source.is_relative_to(destination):
        raise ValueError("Export destination must not contain the source")
    if destination.is_symlink():
        raise ValueError("Export destination must not be a symlink")
    stage = Path(tempfile.mkdtemp(prefix=f".{name}-", dir=output))
    try:
        hashes = {}
        for path, relative in files:
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            if digest != hashlib.sha256(path.read_bytes()).hexdigest():
                raise ValueError(f"Source changed while packaging: {relative}")
            hashes[relative.as_posix()] = digest
        warnings = ["Dependency metadata describes registry relationships, not a verified execution closure.",
                    "Host tools and repository-external resources have not been validated."]
        if dependencies:
            warnings.append("Related skills are not bundled: " + ", ".join(dependencies))
        if not entry:
            warnings.append("Skill is not registered; dependency metadata is unknown.")
        manifest = {
            "format_version": 1,
            "skill": {"name": name, "version": version,
                      "description": metadata.get("description") or entry.get("description", ""),
                      "type": entry.get("type") or sync.infer_type(name, text, metadata),
                      "source": entry.get("source", "custom")},
            "metrics": {**sync.compute_metrics(text, source),
                        "auto_score": entry.get("auto_score", 0)},
            "dependencies": {"depends_on": dependencies,
                             "required_scripts": entry.get("required_scripts", []),
                             "required_data": entry.get("required_data", []),
                             "validation_status": "unverified",
                             "not_bundled": dependencies,
                             "unknown_skills": [d for d in dependencies if d not in registry.get("skills", {})]},
            "exported_from": {"plugin": entry.get("plugin", "unknown"),
                              "plugin_version": registry.get("plugin_version", "unknown"),
                              "git_revision": revision,
                              "working_tree_dirty": dirty,
                              "export_date": datetime.now(timezone.utc).date().isoformat()},
            "files": hashes,
            "self_contained": False,
            "warnings": warnings,
        }
        (stage / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        # Keep an authored README intact; installation notes live in the manifest
        # when one is already present.
        if not (stage / "README.md").exists():
            (stage / "README.md").write_text(
                f"# {name}\n\nCopy this bundle into your agent's skills directory as `{name}/`.\n"
                "Check manifest.json for file hashes, source revision, and unresolved dependencies.\n"
                "This snapshot does not establish that all required host tools or external resources are available.\n")
        # Preserve the previous valid bundle if promotion fails.
        backup = None
        if destination.exists():
            backup = Path(tempfile.mkdtemp(prefix=f".{name}-previous-", dir=output))
            backup.rmdir()
            destination.rename(backup)
        try:
            stage.rename(destination)
        except OSError:
            if backup is not None:
                backup.rename(destination)
            raise
        if backup is not None:
            shutil.rmtree(backup)
        return {"skill": name, "export_dir": str(destination), "files": len(hashes), "warnings": warnings}
    finally:
        if stage.exists():
            shutil.rmtree(stage)


if __name__ == "__main__":
    try:
        if len(sys.argv) not in {2, 3}:
            raise ValueError("Usage: package-skill.sh <skill-dir> [output-dir]")
        print(json.dumps(package(Path(sys.argv[1]), Path(sys.argv[2]) if len(sys.argv) == 3 else ROOT / "exports")))
    except (ValueError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
