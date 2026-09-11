# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['rapidocr_onnxruntime']
hiddenimports += collect_submodules('rapidocr_onnxruntime')


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('appraiser_config.json', '.'), ('E:\\Project\\MACROOOOOOOOO\\fisch_appraiser\\venv\\Lib\\site-packages\\rapidocr_onnxruntime\\config.yaml', 'rapidocr_onnxruntime'), ('E:\\Project\\MACROOOOOOOOO\\fisch_appraiser\\venv\\Lib\\site-packages\\rapidocr_onnxruntime\\models', 'rapidocr_onnxruntime\\models')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FischAppraiser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
