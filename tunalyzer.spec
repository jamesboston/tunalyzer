# -*- mode: python -*-

# see http://www.pyinstaller.org/ticket/14

from distutils.sysconfig import get_python_lib

gtkdir = os.path.join(get_python_lib(), 'gtk-2.0', 'runtime')
gtkrc_dir = os.path.join('share', 'themes', 'MS-Windows', 'gtk-2.0')
engines_dir = os.path.join('lib', 'gtk-2.0', '2.10.0', 'engines')

extra_datas = [ ('gtkrc', os.path.join(gtkdir, gtkrc_dir, 'gtkrc'), 'DATA'), \
                ('tunalyzer.xml', 'src\\tunalyzer.xml', 'DATA')]

extra_binaries = [ (os.path.join(engines_dir, 'libwimp.dll'), \
                   os.path.join(gtkdir, engines_dir, 'libwimp.dll'), 'BINARY') ]

a = Analysis(['src\\tunalyzer.py'],
             pathex=['C:\\Users\\James\\Documents\\Code\\Tunalyzer\\pyinstaller'],
             hiddenimports=['gtkglext', 'gdkgl', 'gdkglext', 'gdk', 'gtk.gdk', 'gtk.gtkgl',
                 'gtk.gtkgl._gtkgl', 'gtkgl', 'pangocairo', 'pango', 'atk',
                 'gobject', 'gtk.glade', 'cairo', 'gio',
                 'gtk.keysyms'],
             hookspath=None)

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          a.binaries + extra_binaries,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\tunalyzer', 'tunalyzer.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas + extra_datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'tunalyzer'))

app = BUNDLE(coll, name=os.path.join('dist', 'tunalyzer.app'))
