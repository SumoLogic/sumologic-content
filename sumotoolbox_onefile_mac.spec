# -*- mode: python -*-

block_cipher = None

added_files = [
    ( 'data/sumotoolbox.ui', 'data' ),
    ( 'data/sumotoolbox.ini', 'data'),
    ( 'data/sumotoolbox_logo_small.png', 'data'),
    ( 'data/folder.svg', 'data' ),
    ( 'data/dashboard.svg', 'data' ),
    ( 'data/logsearch.svg', 'data' ),
    ( 'data/scheduledsearch.svg', 'data' ),
    ( 'data/correlationrules.svg', 'data' ),
    ( 'data/informationmodel.svg', 'data' ),
    ( 'data/lookuptable.svg', 'data' ),
    ( 'data/parser.svg', 'data' ),
    ( 'data/collector.ui', 'data' ),
    ( 'data/content.ui', 'data' ),
    ( 'data/field_extraction_rule.ui', 'data' ),
    ( 'data/scheduled_view.ui', 'data' ),
    ( 'qtmodern', 'qtmodern' )
    ]

a = Analysis(['sumotoolbox.py'],
             pathex=['/mnt/tim/PycharmProjects/sumotoolbox'],
             binaries=None,
             datas=added_files,
             hiddenimports=['pkg_resources.py2_warn'],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='sumotoolbox',
          debug=False,
          strip=None,
          upx=True,
          console=False )
