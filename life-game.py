#!/usr/bin/python

import signal
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:

    def __init__(self):
        self.window_is_hidden = False

    def onNew(self, status):
        status.set_text("Started a new grid")

    def onRand(self, status):
        status.set_text("Created a random grid")

    def onLoad(self, status):
        status.set_text("Unimplemented yet...")

    def onSave(self, status):
        status.set_text("Unimplemented yet...")

    def onNext(self, status):
        status.set_text("Next generation")

    def onToggleAuto(self, status):
        tb = builder.get_object('toggleAuto')
        if tb.get_active():
            status.set_text("Auto playing")
        else:
            status.set_text("Stopped")

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
