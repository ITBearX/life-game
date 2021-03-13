#!/usr/bin/python

import signal
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:

    def __init__(self):
        self.window_is_hidden = False

    def onQuit(self, *args):
        Gtk.main_quit()

# Handle pressing Ctr+C properly, ignored by default
signal.signal(signal.SIGINT, signal.SIG_DFL)

builder = Gtk.Builder()
builder.add_from_file('life-game.glade')
builder.connect_signals(Handler())

window = builder.get_object('window_main')
window.show_all()

Gtk.main()
