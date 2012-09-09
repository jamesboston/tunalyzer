# -*- mode: python -*-

# see http://www.pyinstaller.org/ticket/14

import _winreg
import msvcrt


# try:
    # k = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\GTK2-Runtime')
# except EnvironmentError:
    # print 'You must install the Gtk+ 2.2 Runtime Environment to run this program'
    # while not msvcrt.kbhit():
        # pass
    # sys.exit(1)
# else:
    # gtkdir = str(_winreg.QueryValueEx(k, 'InstallationDirectory')[0])
    # gtkversion = str(_winreg.QueryValueEx(k, 'BinVersion')[0])

gtkdir="C:\\Python27_ActiveState\\Lib\\site-packages\\gtk-2.0\\runtime"

#Then we want to go to the directory where the gtkrcfile is located
gtkrc_dir = os.path.join('share', 'themes', 'MS-Windows', 'gtk-2.0')
engines_dir = os.path.join('lib', 'gtk-2.0', '2.10.0', 'engines')


#Add gtkrc file to exe
extra_datas = [ ('gtkrc', os.path.join(gtkdir, gtkrc_dir, 'gtkrc'), 'DATA'), \
                ('tunalyzer.xml', '..\\src\\tunalyzer.xml', 'DATA')]

#Add libwimp.dll to exe (needed for the MS-Windows theme)
extra_binaries = [ (os.path.join(engines_dir, 'libwimp.dll'), \
                   os.path.join(gtkdir, engines_dir, 'libwimp.dll'), 'BINARY') ]

a = Analysis(['..\\src\\tunalyzer.py'],
             pathex=['C:\\Users\\James\\Documents\\Code\\Tunalyzer\\pyinstaller-2.0'],
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
app = BUNDLE(coll,
             name=os.path.join('dist', 'tunalyzer.app'))
