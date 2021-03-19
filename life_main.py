#!/usr/bin/python

import signal
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from life_cairo import LifeGridCairo


class Handler:

    def onNew(self, *args):
        life.zeros()
        self.update_drawing('Created an empty grid')

    def onRand(self, *args):
        life.rand(controls['alive_perc'].get_value()/100)
        self.update_drawing('Created a random grid')

    def onLoad(self, *args):
        status.set_text('Unimplemented yet...')

    def onSave(self, *args):
        status.set_text('Unimplemented yet...')

    def onNext(self, *args):
        life.next_gen()
        self.update_drawing('Next generation')

    def onToggleAuto(self, *args):
        tb = builder.get_object('toggleAuto')
        if tb.get_active():
            t = time.Timer(1.0, autoplay)
            t.start()
            status.set_text('Auto playing')
        else:
            status.set_text('Stopped')

    def onDraw(self, area, context):
        width = area.get_allocated_width()
        height = area.get_allocated_height()
        life.draw(context, width, height)

    def onGridClick(self, area, event):
        life.flip_on_click(event.x, event.y)
        status.set_text('Mouse clicked... at {},{}'.format(event.x, event.y))
        drawing_area.queue_draw()

    def onShapeChange(self, *args):
        rows = controls['rows'].get_value()
        cols = controls['cols'].get_value()
        life.resize(int(rows), int(cols))

        life.h_wrap = controls['h_wrap'].get_active()
        life.v_wrap = controls['v_wrap'].get_active()
        self.update_drawing('Grid shape changed')

    def onRulesChange(self, *args):
        if controls['moore'].get_active():
            life.nbr_func = life.moore_nbr
        elif controls['von_neumann'].get_active():
            life.nbr_func = life.von_neumann_nbr

        a_nbr_min = controls['alive_nbr_min'].get_value()
        a_nbr_max = controls['alive_nbr_max'].get_value()
        if a_nbr_min <= a_nbr_max:
            (life.alive_nbr_min, life.alive_nbr_max) = (a_nbr_min, a_nbr_max)
        else:
            controls['alive_nbr_min'].set_value(life.alive_nbr_min)
            controls['alive_nbr_max'].set_value(life.alive_nbr_max)

        b_nbr_min = controls['birth_nbr_min'].get_value()
        b_nbr_max = controls['birth_nbr_max'].get_value()
        if b_nbr_min <= b_nbr_max:
            (life.birth_nbr_min, life.birth_nbr_max) = (b_nbr_min, b_nbr_max)
            status.set_text('New rules applied')
        else:
            controls['birth_nbr_min'].set_value(life.birth_nbr_min)
            controls['birth_nbr_max'].set_value(life.birth_nbr_max)

        status.set_text('New rules applied')

    def onQuit(self, *args):
        Gtk.main_quit()

    def update_drawing(self, msg=''):
        status.set_text(msg)
        drawing_area.queue_draw()


if __name__ == '__main__':

    # Handle pressing Ctr+C properly, ignored by default
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    builder = Gtk.Builder()
    builder.add_from_file('life_main.glade')
    builder.connect_signals(Handler())

    window = builder.get_object('window_main')
    drawing_area = builder.get_object('drawing_area')
    status = builder.get_object('lb_status')

    ctrls_list = ['rows', 'cols', 'h_wrap', 'v_wrap', 'alive_perc',
                  'alive_nbr_min', 'alive_nbr_max',
                  'birth_nbr_min', 'birth_nbr_max',
                  'moore', 'von_neumann']
    controls = {}
    for ctrl_name in ctrls_list:
        controls[ctrl_name] = builder.get_object('ctrl_' + ctrl_name)

    life = LifeGridCairo(rows=int(controls['rows'].get_value()),
                         cols=int(controls['cols'].get_value()),
                         h_wrap=controls['h_wrap'].get_active(),
                         v_wrap=controls['v_wrap'].get_active())

    life.rand(controls['alive_perc'].get_value()/100)

    window.show_all()

    Gtk.main()
