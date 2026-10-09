"""Original offline integrity checker for the distributed research showcase."""
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
files = [p for p in ROOT.rglob('*') if p.is_file()]
allowed = {'.md', '.py', '.txt', '.json', '.gif', '.png', '.svg', '.cff'}
for p in files:
    assert p.name == 'LICENSE' or p.suffix.lower() in allowed, f'Unexpected file: {p}'
    assert not any(s in p.parts for s in ['.git', '__pycache__', 'node_modules']), str(p)
for name in ['README.md', 'CITATION.cff', 'LICENSE', 'requirements.txt', 'docs/mathematical_overview.md', 'docs/verification.md']:
    assert (ROOT/name).is_file(), name

links = 0
for p in ROOT.rglob('*.md'):
    content = p.read_text()
    targets = re.findall(r'(?:src|href)="([^"]+)"', content)
    targets += re.findall(r'\]\(([^)]+)\)', content)
    assert not re.search(r'(?:src="|!\[[^\]]*\]\()https?://', content), 'External image reference'
    for target in targets:
        if target.startswith(('http:', 'https:', 'mailto:')):
            continue
        filepart = target.split('#')[0]
        if not filepart:
            continue
        resolved = (p.parent/filepart).resolve()
        assert resolved.is_relative_to(ROOT), f'Escaping path: {target}'
        assert resolved.is_file(), f'Broken link in {p}: {target}'
        links += 1

manifest = json.loads((ROOT/'results/asset_manifest.json').read_text())
assert len(manifest) == 10
for asset in manifest:
    p = ROOT/asset['path']
    assert p.stat().st_size == asset['bytes']
    with Image.open(p) as im:
        assert im.format == 'GIF' and im.n_frames > 1
        assert list(im.size) == asset['dimensions']
        assert im.n_frames == asset['frames']
        for j in range(im.n_frames):
            im.seek(j)
            im.load()
            assert im.info.get('duration', 0) > 0
for p in ROOT.rglob('*.png'):
    with Image.open(p) as im:
        im.verify()
for p in ROOT.rglob('*.svg'):
    s = p.read_text()
    ET.fromstring(s)
    assert '<script' not in s and '<image' not in s and 'href=' not in s

m = json.loads((ROOT/'results/showcase_metrics.json').read_text())
assert m['checks']['form_identity_absolute_error'] < 1e-10
assert m['checks']['relative_energy_drift'] < 1e-10
assert m['checks']['spectral_cutoff_12_to_14_change_at_epsilon_0_4'] < 1e-8
assert all(row['observed_order'] > 3.8 for row in m['spectral'][1:])
assert [row['epsilon'] for row in m['spectral']] == [.8, .4, .2, .1]
print(f'PASS: {len(files)} files; {links} local file references; 10 valid animations; stored numerical checks.')
print('This checks the supplied outputs. Run build_showcase.py to recompute them.')
