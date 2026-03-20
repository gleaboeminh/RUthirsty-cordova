# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for TOEIC Speaking Practice (Windows single-file EXE)
# Build command:  pyinstaller toeic_speaking.spec

block_cipher = None

a = Analysis(
    ["toeic_speaking.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        "PyQt5.QtWidgets",
        "PyQt5.QtCore",
        "PyQt5.QtGui",
        "PyQt5.QtPrintSupport",
        "PyQt5.sip",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "numpy", "scipy"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="TOEIC_Speaking_Practice",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # no black console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="toeic_icon.ico",
    version_file=None,
)
