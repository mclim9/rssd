# -*- mode: python -*-

block_cipher = None


a = Analysis(['Unity-K144.py'],
             pathex=['C:\\Program Files (x86)\\Python37-32\\DLLs\\dllls', 'C:\\Users\\lim_m\\ownCloud\\ATE\\AA_Code\\RSSD\\rssd\\Unity'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Unity-K144',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , version='version.txt', icon='Unity.ico')
