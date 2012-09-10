'''
Created on Sep 8, 2012

@author: James Boston
'''

import gtk

class Widgets:
    def __init__(self, builder):
        self.widgets = {'window',
                   'aboutdialog',
                   # ui widgets
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

        for w in self.widgets:
            setattr (self, w, builder.get_object(w))

        # used in add_row and initial_sort
        self.stores = {'albums': self.albumstore,
                       'songs': self.songstore,
                       'artists': self.artiststore,
                       'years': self.yearstore}

        # setup TreeViewColumns         
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

    def clear_lists(self):
        self.songstore.clear()
        self.albumstore.clear()
        self.artiststore.clear()
        self.yearstore.clear()

    def add_row(self, store, row):
        self.stores[store].append(row)

    def initial_sort(self):
        for store in self.stores.values():
            store.set_sort_column_id(0, gtk.SORT_DESCENDING)

    def start_button_down(self, state):
        if state is True:
            self.comboboxplaylist.set_button_sensitivity(gtk.SENSITIVITY_OFF)
            self.startbutton.set_relief(gtk.RELIEF_NONE)
            text = self.comboboxplaylist.get_active_text()
            self.statusbar.set_text('Status: Analyzing playlist \'' + text + '\'. This may take a few moments.')
        else:
            self.statusbar.set_text('Status: Ready')
            self.comboboxplaylist.set_button_sensitivity(gtk.SENSITIVITY_ON)
            self.startbutton.set_relief(gtk.RELIEF_NORMAL)

    def get_playlist(self):
        return self.comboboxplaylist.get_active_text()

    def close_main_window(self):
        gtk.main_quit()

    def show_main_window(self):
        self.window.show()

    def get_active(self):
        return self.comboboxplaylist.get_active()

    def set_active_playlist_dropdown(self, num):
        self.comboboxplaylist.set_active(num)

    def append_playlist_dropdown(self, data):
        self.playliststore.append(data)

    def show_about(self):
        response = self.aboutdialog.run()
        if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_CANCEL:
            self.aboutdialog.hide()
