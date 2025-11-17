# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['CameraMonitor_Final_v7.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('sky-tech logo.png', '.'),
        ('ip.xlsx', '.'),
        ('update_manager.py', '.'),
        ('updater.exe', '.'),
        ('version_config.json', '.'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'pandas',
        'openpyxl',
        'requests',
        'keyring',
        'xml.etree.ElementTree',
        'update_manager',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='NARONG_CCTV_TEAM_v8.4.3',
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
    icon='sky-tech logo.png',
)
