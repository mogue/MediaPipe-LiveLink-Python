# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[ ('src/face_landmarker_v2_with_blendshapes.task', 'src') ],
    hiddenimports=['pyi_splash'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)
pyz = PYZ(a.pure)
splash = Splash(
    'img/splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=(10, 590),
    text_size=10,
    text_color='white',
    minify_script=True,
    always_on_top=True
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    splash,
    splash.binaries,
    [],
    name='WebCam_LiveLink',
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
    icon='img/icon.ico'
)
