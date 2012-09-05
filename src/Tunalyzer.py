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

class MusicStore:
    def __init__(self, widget, itunes):
        self.widget = widget
        self.itunes = itunes
        self.artists = {}
        self.albums = {}
        self.songs = {}
        self.years = {}

    def startover(self):
        self.songs.clear()
        self.artists.clear()
        self.albums.clear()
        self.years.clear()
        self.widget.songstore.clear()
        self.widget.albumstore.clear()
        self.widget.artiststore.clear()
        self.widget.yearstore.clear()

    def addTracks(self):
        count = self.itunes.getPlaylistSize()

        for i in range(1, count):
            track = self.itunes.getTrack(i)

            if track['albumartist']:
                artist = track['albumartist']
            else:
                artist = track['artist']
            song = track['song']
            album = track['album']
            year = track['year']
            playcount = track['playcount']

            time_parts = track['time'].split(":")
            time_parts.reverse()
            secs = int(time_parts[0])
            mins = int(time_parts[1])
            if len(time_parts) > 2:
                hrs = int(time_parts[2])
            else:
                hrs = 0
            play_time = timedelta(seconds=secs, minutes=mins, hours=hrs) * playcount

            if self.artists.has_key(artist):
                self.artists[artist]['playcount'] += playcount
                self.artists[artist]['time'] += play_time
            else:
                self.artists[artist] = {'playcount': playcount, 'time': play_time}

            if self.years.has_key(year):
                self.years[year]['playcount'] += playcount
                self.years[year]['time'] += play_time
            else:
                self.years[year] = {'playcount': playcount, 'time': play_time}

            if self.songs.has_key((song, artist)):
                self.songs[(song, artist)]['playcount'] += playcount
                self.songs[(song, artist)]['time'] += play_time
            else:
                self.songs[song, artist] = {'playcount': playcount, 'time': play_time}

            if self.albums.has_key((album, artist)):
                self.albums[(album, artist)]['playcount'] += playcount
                self.albums[(album, artist)]['time'] += play_time
            else:
                self.albums[(album, artist)] = {'playcount': playcount, 'time': play_time}

#    def _limit(self, data):
#        keys = data.keys()
#        keys = sorted(keys, key=lambda x:data[x]['time'])
#        keys.reverse()
#        return keys

    def liszterize(self):
        """
        rows are timedelta, play count, total play time, ....
            
        """

        for artist in self.artists:
            row = self.artists[artist]['time'].total_seconds(), self.artists[artist]['playcount'], str(self.artists[artist]['time']), artist
            self.widget.artiststore.append(row)
        self.widget.artiststore.set_sort_column_id(0, gtk.SORT_DESCENDING)

        for album in self.albums:
            row = (self.albums[album]['time'].total_seconds(), self.albums[album]['playcount'], str(self.albums[album]['time'])) + album
            self.widget.albumstore.append(row)
        self.widget.albumstore.set_sort_column_id(0, gtk.SORT_DESCENDING)

        for song in self.songs:
            if isinstance(song, basestring):
                row = self.songs[song]['time'].total_seconds(), self.songs[song]['playcount'], str(self.songs[song]['time']), song
            else:
                row = (self.songs[song]['time'].total_seconds(), self.songs[song]['playcount'], str(self.songs[song]['time'])) + song
            self.widget.songstore.append(row)
        self.widget.songstore.set_sort_column_id(0, gtk.SORT_DESCENDING)

        for year in self.years:
            row = self.years[year]['time'].total_seconds(), self.years[year]['playcount'], str(self.years[year]['time']), year
            self.widget.yearstore.append(row)
        self.widget.yearstore.set_sort_column_id(0, gtk.SORT_DESCENDING)

class iTunesApp:
    def __init__(self):
        self.app = win32com.client.gencache.EnsureDispatch("iTunes.Application")
        self.mainLibrarySource = self.app.LibrarySource

    def getPlayLists(self):
        self.playLists = self.mainLibrarySource.Playlists
        self.numPlayLists = self.playLists.Count
        pList = []
        for p in range(1, self.numPlayLists):
            if not self.playLists.Item(p).Name in ('Library', 'Movies', 'Podcasts', 'Books', 'Purchased', 'Genius', 'iTunes DJ'):
                pList.append(self.playLists.Item(p).Name)
        return pList

    def setPlaylist(self, name="Music"):
        for i in range(1, self.numPlayLists):
            self.playList = self.playLists.Item(i)
            if self.playList.Name == name:
                self.tracks = self.playList.Tracks
                self.trackCount = self.tracks.Count
                break
            self.playList = None

        if self.playList:
            return True
        else:
            return False

    def getPlaylistSize(self):
        return self.trackCount

    def getTrack(self, num):
        track = self.tracks.Item(num)
        track = win32com.client.CastTo(track, "IITFileOrCDTrack")
        parsedTrack = {'artist': track.Artist,
                       'albumartist': track.AlbumArtist,
                       'album': track.Album,
                       'song': track.Name,
                       'time': track.Time,
                       'playcount': track.PlayedCount,
                       'year': track.Year }
        return parsedTrack

class Handlers:
    def __init__(self, widget, itunes, model):
        self.widget = widget
        self.itunes = itunes
        self.model = model

    def on_startbutton_clicked (self, *args):
        if self.widget.comboboxplaylist.get_active():
            self.widget.comboboxplaylist.set_button_sensitivity(gtk.SENSITIVITY_OFF)
            self.widget.startbutton.set_relief(gtk.RELIEF_NONE)
            text = self.widget.comboboxplaylist.get_active_text()
            self.widget.statusbar.set_text('Status: Analyzing playlist \'' + text + '\'. This may take a few moments.')
            self.model.startover()
            self.itunes.setPlaylist(text)
            self.model.addTracks()
            self.model.liszterize()
            self.widget.statusbar.set_text('Status: Ready')
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
        views = { self.treeViewArtists: ('Plays', 'Time', 'Artist'),
                 self.treeViewAlbums: ('Plays', 'Time', 'Album', 'Artist'),
                 self.treeViewSongs: ('Plays', 'Time', 'Song', 'Artist'),
                 self.treeViewYears: ('Plays', 'Time', 'Year') }

        renderer = gtk.CellRendererText()
        for view in views:
            columns = views[view]
            pos = 1
            for name in columns:
                viewcolumn = gtk.TreeViewColumn(name, renderer, text=pos)
                if name == 'Time':
                    viewcolumn.set_sort_column_id(0)
                else:
                    viewcolumn.set_sort_column_id(pos)
                viewcolumn.set_resizable(True)
                viewcolumn.pack_start(renderer)
                view.append_column(viewcolumn)
                pos = pos + 1

        self.comboboxplaylist.pack_start(renderer)
        self.comboboxplaylist.add_attribute(renderer, "text", 0)
        self.playliststore.append(["--- Select Playlist ---"])

class Tunalyzer:
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file('tunalyzer.xml')
        self.widgets = Widgets(builder)
        self.itunes = iTunesApp()
        self.music = MusicStore(self.widgets, self.itunes)
        builder.connect_signals(Handlers(self.widgets, self.itunes, self.music))
        self.populateDropDown() # TODO: this should be a handler / window create signal?
        self.widgets.statusbar.set_text('Status: Ready')
        self.widgets.window.show()

    def populateDropDown(self):
        pList = self.itunes.getPlayLists()
        i = 1
        for p in pList:
            self.widgets.playliststore.append([p])
            i = i + 1
        self.widgets.comboboxplaylist.set_active(0)

if __name__ == "__main__":
    tuna = Tunalyzer()
    gtk.main()
