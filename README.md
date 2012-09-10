# Tunalyzer

Analyze your iTunes library. Find out how many minutes you have listened to a song, an artist, an album, or a music 
from a particular year.
 

![tunalyzer](https://raw.github.com/jamesboston/tunalyzer/master/screenshot.png)

## Usage

1. Start iTunes.
2. Start Tunalyzer
3. Select playlist
4. Push start

## Development

### Building

The build process assumes that PyGtk is in your Python site-packages.

From the project root:<br />
`python pyinstaller\utils\Build.py tunalyzer.spec`

Completed build is in `dist\tunalyzer` directory.

#### Prerequisites

* Python 2.7
	* Windows COM extensions for Python 
	* see [http://www.python.org/download/windows/](http://www.python.org/download/windows/)
* [PyGtk](http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.24/)
* PyInstaller (included as git submodule)

###Feature wish list:

* exporting song analysis as a playlist
* support MacOS by using AppleScript in the itunes module
* support Linux with a module for scripting Rhythmbox (or Banshee?)
* saving analysis history
* graphing of analysis
* alternate ncurses or web frontend
* support building and/or packaging on Mac and Linux
* update checking


## License

[GPLv3](https://github.com/jamesboston/tunalyzer/blob/master/LICENSE.md) 