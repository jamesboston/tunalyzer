#
#
#    Tunalyzer - analyzes your iTunes library and outputs statistics
#    by James Boston
#    Copyright (C) 2012.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from datetime import timedelta
import win32com.client
import gtk
#import gobject

class MusicModel(dict):
    def __init__(self, *args, **kwargs):
        super(MusicModel, self).__init__(*args, **kwargs)

    def add(self, playTime, playCount, keya, keyb=None):
        timeParts = playTime.split(":")
        timeParts.reverse()
        secs = int(timeParts[0])
        mins = int(timeParts[1])
        if len(timeParts) > 2:
            hrs = int(timeParts[2])
        else:
            hrs = 0
        pTime = timedelta(seconds=secs, minutes=mins, hours=hrs)

        if keyb:
            key = keya, keyb
        else:
            key = keya

        if self.has_key(key):
            pTime += self[key][0]
            playCount += self[key][1]

        self[key] = pTime, playCount

    def liszterize(self):
        liszt = []
        for key in self:
            if isinstance(key, basestring):
                liszt.append((str(self[key][0]), self[key][1]) + (key,))
            else:
                liszt.append((str(self[key][0]), self[key][1]) + key)

        return sorted(liszt, key=lambda x:(x[0]).lower())

class iTunesApp:
    def __init__(self):
        self.app = win32com.client.gencache.EnsureDispatch("iTunes.Application")
        self.mainLibrarySource = self.app.LibrarySource

        self.artists = MusicModel()
        self.years = MusicModel()
        self.albums = MusicModel()
        self.songs = MusicModel()

    def getPlayLists(self):
        self.playLists = self.mainLibrarySource.Playlists
        self.numPlayLists = self.playLists.Count
        pList = []
        for p in range(1, self.numPlayLists):
            pList.append(self.playLists.Item(p).Name)
        return pList

    def setPlaylist(self, name="Music"):
        for i in range(1, self.numPlayLists):
            self.playList = self.playLists.Item(i)
            if self.playList.Name == name:
                self.tracks = self.playList.Tracks
                self.trackCount = self.tracks.Count
                break
            self.playList = "Not found"

        if self.playList == "Not found":
            return 0
        else:
            self.__analyze()
            return 1


    def __analyze(self):
        for i in range(1, self.trackCount):
            track = self.tracks.Item(i)

            artist = track.Artist
            album = track.Album
            name = track.Name
            playTime = track.Time
            playCount = track.PlayedCount
            trackYear = track.Year

            self.artists.add(playTime, playCount, artist)
            self.years.add(playTime, playCount, trackYear)
            self.albums.add(playTime, playCount, album, artist)
            self.songs.add(playTime, playCount, name, artist)

    def spew(self):
        a = self.albums.liszterize()
        return a


class Handlers:

    def __init__(self, widget, itunes):
        self.widget = widget
        self.itunes = itunes

    def on_startbutton_clicked (self, *args):
        if self.widget.comboboxplaylist.get_active():
            self.widget.comboboxplaylist.set_button_sensitivity(gtk.SENSITIVITY_OFF)
            self.widget.startbutton.set_relief(gtk.RELIEF_NONE)
            text = self.widget.comboboxplaylist.get_active_text()
            self.widget.statusbar.set_text('Status: Analyzing playlist \'' + text + '\'. This may take a few moments.')
            self.itunes.setPlaylist(text)

            artists = self.itunes.artists.liszterize()
            i = 1
            for artist in artists:
                self.widget.artiststore.append(artist)
                i = i + 1

            self.widget.comboboxplaylist.set_button_sensitivity(gtk.SENSITIVITY_ON)
            self.widget.startbutton.set_relief(gtk.RELIEF_NORMAL)

    def main_quit (self, data=None):
        gtk.main_quit()

    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()

def delete_event(self, widget, event, data=None):
    gtk.main_quit()

class Widgets:
    
    def __init__(self, builder):
        widgets = {'window',
                   # widget widgets
                   'comboboxplaylist',
                   'treeViewSongs',
                   'treeViewAlbums',
                   'treeViewArtists',
                   'treeViewYears',
                   'statusbar',
                   'startbutton',
                   # data stores
                   'playliststore',
                   'albumstore',
                   'songstore',
                   'artiststore',
                   'yearstore'}
        
        for w in widgets:
            setattr (self, w, builder.get_object(w))
        
        # attach TreeViewColumns to ListStores        
        views = { self.treeViewArtists: (('Artist', 2), ('Plays', 1), ('Time', 0)),
                 self.treeViewAlbums: (('Album', 2), ('Artist', 3), ('Plays', 1), ('Time', 0)),
                 self.treeViewSongs: (('Song', 2), ('Artist', 3), ('Plays', 1), ('Time', 0)),
                 self.treeViewYears: (('Year', 2), ('Plays', 1), ('Time', 0)) }

        renderer = gtk.CellRendererText()
        for view in views:
            columns = views[view]
            for data in columns:
                name = data[0]
                pos = data[1]
                viewcolumn = gtk.TreeViewColumn(name, renderer, text=pos)
                viewcolumn.set_sort_column_id(pos)
                viewcolumn.pack_start(renderer)
                view.append_column(viewcolumn)

        self.comboboxplaylist.pack_start(renderer)
        self.comboboxplaylist.add_attribute(renderer, "text", 0)
        self.playliststore.append(["--- Select Playlist ---"])

class Tunalyzer:

    def __init__(self):

        builder = gtk.Builder()
        builder.add_from_file('tunalyzer.xml')
        self.w = Widgets(builder)
        self.itunes = iTunesApp()
        builder.connect_signals(Handlers(self.w, self.itunes))
        self.populateDropDown() # TODO: this should be a handler / window create signal?
        self.w.window.show()

    def populateDropDown(self):
        pList = self.itunes.getPlayLists()
        i = 1
        for p in pList:
            self.w.playliststore.append([p])
            i = i + 1
        self.w.comboboxplaylist.set_active(0)

if __name__ == "__main__":
    tuna = Tunalyzer()
    gtk.main()

