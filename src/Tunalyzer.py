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

import os, sys
import gtk
import itunes
import models
import views
import controllers


if __name__ == "__main__":

    try:
        basedir = os.environ['_MEIPASS2']
    except KeyError:
        basedir = sys.path[0]

    #Use embedded gtkrc
    gtkrc = os.path.join(basedir, 'gtkrc')
    gtk.rc_set_default_files([gtkrc])
    gtk.rc_reparse_all_for_settings(gtk.settings_get_default(), True)

    builder = gtk.Builder()
    builder.add_from_file(os.path.join(basedir, 'tunalyzer.xml'))
    model = models.MusicStore(itunes.iTunesApp())
    view = views.Widgets(builder)
    handler = controllers.Handlers(view, model)
    builder.connect_signals(handler)
    view.show_main_window()

    gtk.main()
