"""Exercise portable delivery through real MCP transports in a disposable library."""
import asyncio
import base64
import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path

import httpx
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ('color-theory', 'design-orchestrator', 'spelunker')


@pytest.mark.parametrize('transport', ['stdio', 'http'])
def test_portable_delivery_over_transport(tmp_path, transport):
    server_dir = tmp_path / 'mcp-server'
    server_dir.mkdir()
    for file in (ROOT / 'mcp-server').glob('*.py'):
        shutil.copy2(file, server_dir / file.name)
    (tmp_path / 'data').mkdir()
    registry = json.loads((ROOT / 'data/registry.json').read_text())
    (tmp_path / 'data/registry.json').write_text(json.dumps(registry))
    for name in SKILLS:
        directory = Path(registry['skills'][name]['location']).parent
        shutil.copytree(ROOT / directory, tmp_path / directory)
    # Build through the actual CLI; no destination library or live telemetry changes.
    bundles = {}
    for name in SKILLS:
        source = tmp_path / Path(registry['skills'][name]['location']).parent
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/package_skill.py'),
                                 str(source), str(tmp_path / 'exports')],
                                capture_output=True, text=True, check=True)
        bundles[name] = Path(json.loads(result.stdout)['export_dir'])

    async def inspect(read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            names = {tool.name for tool in (await session.list_tools()).tools}
            assert {'list_skill_files', 'get_skill_file', 'get_skill'} <= names
            assert 'rebuild_search_index' not in names
            for name in SKILLS:
                listing = await session.call_tool('list_skill_files', {'skill_name': name})
                assert not listing.isError
                files = json.loads(listing.content[0].text)['files']
                manifest = json.loads((bundles[name] / 'manifest.json').read_text())
                assert {f['path']: f['sha256'] for f in files} == manifest['files']
                for file in files:
                    response = await session.call_tool('get_skill_file', {
                        'skill_name': name, 'relative_path': file['path']})
                    assert not response.isError
                    payload = json.loads(response.content[0].text)
                    raw = payload['content'].encode('utf-8') if payload['encoding'] == 'utf-8' else base64.b64decode(payload['content'])
                    assert raw == (bundles[name] / file['path']).read_bytes()
                    assert hashlib.sha256(raw).hexdigest() == payload['sha256']
            # An absent capability stays absent; no implied write or execution surface.
            missing = await session.call_tool('execute_skill', {'skill_name': 'spelunker'})
            assert missing.isError
            invalid = await session.call_tool('get_skill_file', {
                'skill_name': 'spelunker', 'relative_path': '../SKILL.md'})
            assert 'Invalid' in invalid.content[0].text

    async def run():
        env = {**os.environ, 'MCP_REMOTE': 'true', 'MCP_READ_ONLY': '1',
               'TELEMETRY_FIRESTORE': '0'}
        if transport == 'stdio':
            params = StdioServerParameters(command=sys.executable,
                args=[str(server_dir / 'server.py'), '--transport', 'stdio'], env=env)
            async with stdio_client(params) as (read, write):
                await inspect(read, write)
        else:
            with socket.socket() as sock:
                sock.bind(('127.0.0.1', 0))
                port = sock.getsockname()[1]
            url = f'http://127.0.0.1:{port}/mcp'
            with (tmp_path / 'server.log').open('w') as log:
                proc = subprocess.Popen([sys.executable, str(server_dir / 'server.py'),
                    '--remote', '--host', '127.0.0.1', '--port', str(port)],
                    env=env, stdout=log, stderr=log)
                try:
                    async with httpx.AsyncClient(timeout=1) as client:
                        for _ in range(100):
                            if proc.poll() is not None:
                                pytest.fail((tmp_path / 'server.log').read_text())
                            try:
                                await client.get(url)
                                break
                            except httpx.ConnectError:
                                await asyncio.sleep(0.1)
                        else:
                            pytest.fail('MCP server did not start')
                    async with streamable_http_client(url) as (read, write, _):
                        await inspect(read, write)
                finally:
                    proc.terminate()
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                        proc.wait()
    asyncio.run(run())
