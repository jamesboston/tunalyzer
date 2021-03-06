## DISCONTINUED

Development stopped. This software was made for a world before streaming music services were so ubiquitous. 


# Tunalyzer

Analyze your iTunes library. Find out how many minutes you have listened to a song, an artist, an album, or a music 
from a particular year.
 

![tunalyzer](https://raw.github.com/jamesboston/tunalyzer/master/screenshot.png)

## Usage

1. Start iTunes.
2. Start Tunalyzer
3. Select playlist
4. Push start

### Download installer or zip:
[https://github.com/jamesboston/tunalyzer/downloads](https://github.com/jamesboston/tunalyzer/downloads)

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


## License

[GPLv3](https://github.com/jamesboston/tunalyzer/blob/master/LICENSE.md) 
