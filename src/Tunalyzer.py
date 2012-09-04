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
import gobject
     
class MusicDict(dict):
    def __init__(self, *args, **kwargs):
        super(MusicDict, self).__init__(*args, **kwargs)
  
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
        
        self.artists = MusicDict()
        self.years = MusicDict()
        self.albums = MusicDict()
        self.songs = MusicDict()        
        
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
    
   
class Handler:
    
    def __init__(self, data):
        self.ui = data
        
    def on_startbutton_clicked (self, *args):
        if self.ui.comboboxplaylist.get_active():
            self.ui.comboboxplaylist.set_button_sensitivity(gtk.SENSITIVITY_OFF)
            self.ui.startbutton.set_relief(gtk.RELIEF_NONE)
            text = self.ui.comboboxplaylist.get_active_text()
            self.ui.statusbar.set_text('Status: Analyzing playlist \'' + text + '\'. This may take a few moments.')
            self.ui.tunes.setPlaylist(text)
                   
            artists = self.ui.tunes.artists.liszterize()
            i=1
            for artist in artists:
                self.ui.artiststore.append(artist)
                i = i + 1
            
            self.ui.comboboxplaylist.set_button_sensitivity(gtk.SENSITIVITY_ON)
            self.ui.startbutton.set_relief(gtk.RELIEF_NORMAL)
            
        
    def main_quit (self, data=None):
        gtk.main_quit()         

    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()

def delete_event(self, widget, event, data=None):
    gtk.main_quit()

class TunaWindow:
     
    def __init__(self):  
      
        builder = gtk.Builder()
        builder.add_from_file('tunalyzer.xml')       
         
        self.window = builder.get_object('tunawindow')

        # stores
        self.playliststore = builder.get_object('playliststore')
        self.albumstore = builder.get_object('albumstore')
        self.artiststore = builder.get_object('artiststore')
        self.songstore = builder.get_object('songstore')
        self.yearstore = builder.get_object('yearstore')

        # widgets
        self.comboboxplaylist = builder.get_object('comboboxplaylist')
        self.treeViewSongs = builder.get_object('treeViewSongs')
        self.treeViewAlbums = builder.get_object('treeViewAlbums')
        self.treeViewArtists = builder.get_object('treeViewArtists')
        self.treeViewYears = builder.get_object('treeViewYears')
        self.statusbar = builder.get_object('statusbar')
        self.startbutton = builder.get_object('startbutton')
        
        # add render to columns
        renderer=gtk.CellRendererText()
        artistcolumn = gtk.TreeViewColumn('Artist', renderer, text=2)
        artistcolumn.set_sort_column_id(2)
        artistcolumn.pack_start(renderer)
        self.treeViewArtists.append_column(artistcolumn)
        
        timecolumn = gtk.TreeViewColumn('Time', renderer, text=0)
        timecolumn.set_sort_column_id(0)
        timecolumn.pack_start(renderer)
        self.treeViewArtists.append_column(timecolumn)
        
        playscolumn = gtk.TreeViewColumn('Plays', renderer, text=1)
        playscolumn.set_sort_column_id(1)
        playscolumn.pack_start(renderer)
        self.treeViewArtists.append_column(playscolumn)
        
        # signals
        builder.connect_signals(Handler(self))

        self.window.show()
        self.tunes = iTunesApp()        
        self.populateDropDown()        

        
    def populateDropDown(self):
        renderer=gtk.CellRendererText()
        self.comboboxplaylist.pack_start(renderer)
        self.comboboxplaylist.add_attribute(renderer, "text", 0)
        self.playliststore.append(["--- Select Playlist ---"])    
        
        pList = self.tunes.getPlayLists()
        i=1
        for p in pList:
            self.playliststore.append([p])
            i = i + 1
        self.comboboxplaylist.set_active(0)

if __name__ == "__main__":
    tuna = TunaWindow()
    gtk.main()
    
