'''
Created on Sep 8, 2012

@author: James Boston
'''

from datetime import timedelta

class MusicStore:
    def __init__(self, tunes):
        self.tunes = tunes
        self.artists = {}
        self.albums = {}
        self.songs = {}
        self.years = {}

    def start_over(self):
        self.songs.clear()
        self.artists.clear()
        self.albums.clear()
        self.years.clear()

    def get_playlists(self):
        result = self.tunes.get_playlists()
        return result

    def process_playlist(self, data):
        result = self.tunes.set_playlist(data)
        if not result:
            return False

        count = self.tunes.get_playlist_size()

        for i in range(1, count):
            track = self.tunes.get_track(i)

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
