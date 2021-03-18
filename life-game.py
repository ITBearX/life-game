#!/usr/bin/python

import signal
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from life_cairo import LifeGridCairo


class Handler:

    def __init__(self):
        self.window_is_hidden = False

    def onNew(self, status):
        life.zeros()
        status.set_text("Started a new grid")

    def onRand(self, status):
        life.rand()
        status.set_text("Created a random grid")

    def onLoad(self, status):
        status.set_text("Unimplemented yet...")

    def onSave(self, status):
        status.set_text("Unimplemented yet...")

    def onNext(self, status):
        life.next_gen()
        status.set_text("Next generation")

    def onToggleAuto(self, status):
        tb = builder.get_object('toggleAuto')
        if tb.get_active():
            t = time.Timer(1.0, autoplay)
            t.start()
            status.set_text("Auto playing")
        else:
            status.set_text("Stopped")

    def onDraw(self, area, context):
        width = area.get_allocated_width()
        height = area.get_allocated_height()
        life.draw(context, width, height)

    def onGridClick(self, drawing_area, event):
        status = builder.get_object('lb_status')
        status.set_text("Mouse clicked... at {},{}".format(event.x, event.y))
#        drawing_area.queue_draw()

    def onRulesChange(self, *args):
        pass

    def onShapeChange(self, *args):
        ah = builder.get_object('adjust_height')
        aw = builder.get_object('adjust_width')
        life.resize((int(ah.get_value()), int(aw.get_value())))

    def onPercChange(self, *args):
        pass

    def onQuit(self, *args):
        Gtk.main_quit()


life = LifeGridCairo()
life.rand()

# Handle pressing Ctr+C properly, ignored by default
signal.signal(signal.SIGINT, signal.SIG_DFL)

builder = Gtk.Builder()
builder.add_from_file('life-game.glade')
builder.connect_signals(Handler())

window = builder.get_object('window_main')
window.show_all()

Gtk.main()
