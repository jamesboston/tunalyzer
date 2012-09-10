'''
Created on Sep 5, 2012

@author: James Boston
'''

import win32com.client

class iTunesApp:
    def __init__(self):
        self.app = win32com.client.gencache.EnsureDispatch("iTunes.Application")
        self.library_source = self.app.LibrarySource

    def get_playlists(self):
        self.play_lists = self.library_source.Playlists
        self.num_of_play_lists = self.play_lists.Count
        playlist_naturalized = []
        for p in range(1, self.num_of_play_lists):
            if not self.play_lists.Item(p).Name in ('Library', 'Movies', 'Podcasts', 'Books', 'Purchased', 'Genius',
                                                   'iTunes DJ'):
                playlist_naturalized.append(self.play_lists.Item(p).Name)
        return playlist_naturalized

    def set_playlist(self, name="Music"):
        for i in range(1, self.num_of_play_lists):
            self.play_list = self.play_lists.Item(i)
            if self.play_list.Name == name:
                self.tracks = self.play_list.Tracks
                self.track_count = self.tracks.Count
                break
            self.play_list = None
        return self.play_list is not None

    def get_playlist_size(self):
        return self.track_count

    def get_track(self, num):
        if num > self.track_count:
            return None

        track = self.tracks.Item(num)
        track = win32com.client.CastTo(track, "IITFileOrCDTrack")
        parsed_track = {'artist': track.Artist,
                       'albumartist': track.AlbumArtist,
                       'album': track.Album,
                       'song': track.Name,
                       'time': track.Time,
                       'playcount': track.PlayedCount,
                       'year': track.Year }
        return parsed_track
