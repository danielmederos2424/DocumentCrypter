from pathlib import Path
import os
from PIL import Image

root_dir = Path('.')
png_icon_path = root_dir / 'assets' / 'icon.png'
ico_path = root_dir / 'assets' / 'icon.ico'

if not ico_path.exists() and png_icon_path.exists():
    try:
        img = Image.open(png_icon_path)
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        img.save(ico_path, format='ICO')
    except Exception as e:
        print(f"Warning: Could not convert icon: {e}")
        ico_path = None
else:
    ico_path = ico_path if ico_path.exists() else None

def collect_data_files(start_path):
    data_files = []
    if (root_dir / 'assets').exists():
        data_files.append(('assets', 'assets'))

    for path in root_dir.rglob('*.py'):
        if '__pycache__' not in str(path):
            relative_path = path.relative_to(root_dir)
            parent = str(relative_path.parent)
            if parent == '.':
                continue
            data_files.append((str(path), parent))
    
    return data_files

block_cipher = None
data_files = collect_data_files(root_dir)

a = Analysis(
    ['main.py'],
    pathex=[str(root_dir)],
    binaries=[],
    datas=data_files,
    hiddenimports=['flet', 'crypto', 'gui', 'gui.views'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['__pycache__'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='document-crypter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ico_path if ico_path else None
)