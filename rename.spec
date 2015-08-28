# -*- mode: python -*-
a = Analysis(['rename.py'],
             pathex=['D:\\git_rep\\rename'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='rename.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='VVV.ico')
