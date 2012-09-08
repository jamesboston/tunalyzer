'''
Created on Sep 8, 2012

@author: James Boston
'''


class Handlers:
    def __init__(self, view, model):
        self.view = view
        self.tunes = model
        self.populate_drop_down()

    def on_startbutton_clicked (self, *args):
        def liszterize():
            '''  row order is timedelta, play count, total play time, etc...  '''
            artists = self.tunes.artists
            albums = self.tunes.albums
            songs = self.tunes.songs
            years = self.tunes.years

            for artist in artists:
                row = (artists[artist]['time'].total_seconds(),
                       artists[artist]['playcount'],
                       str(artists[artist]['time']),
                       artist)
                self.view.add_row('artists', row)

            for album in albums:
                row = (albums[album]['time'].total_seconds(),
                       albums[album]['playcount'],
                       str(albums[album]['time'])) + album
                self.view.add_row('albums', row)

            for song in songs:
                if isinstance(song, basestring):
                    row = (songs[song]['time'].total_seconds(),
                           songs[song]['playcount'],
                           str(songs[song]['time']),
                           song)
                else:
                    row = (songs[song]['time'].total_seconds(),
                           songs[song]['playcount'],
                           str(songs[song]['time'])) + song
                self.view.add_row('songs', row)

            for year in years:
                row = (years[year]['time'].total_seconds(),
                       years[year]['playcount'],
                       str(years[year]['time']),
                       year)
                self.view.add_row('years', row)

            self.view.initial_sort()

        if self.view.get_active():
            self.view.start_button_down(True)
            self.tunes.start_over()
            self.view.clear_lists()
            self.tunes.process_playlist(self.view.get_playlist())
            liszterize()
            self.view.start_button_down(False)

    def main_quit (self, data=None):
        self.view.close_main_window()

    def on_window_destroy(self, widget, data=None):
        self.view.close_main_window()

    def populate_drop_down(self):
        pList = self.tunes.get_playlists()
        i = 1
        for p in pList:
            self.view.append_playlist_dropdown([p])            
            i = i + 1
        self.view.set_active_playlist_dropdown(0)
