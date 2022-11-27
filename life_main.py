#!/usr/bin/python

import signal
import time
from threading import Timer
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from life_cairo import LifeGridCairo


class Handler:

    def onDraw(self, area, context):
        width = area.get_allocated_width()
        height = area.get_allocated_height()
        life.draw(context, width, height)

    def onNew(self, *args):
        life.zeros()
        update_drawing('Created an empty grid')

    def onRand(self, *args):
        life.rand(controls['alive_perc'].get_value()/100)
        update_drawing('Created a random grid')

    def onLoad(self, *args):
        f_name = pick_file('Load from file')
        if f_name is not None:
            life.load(f_name)
            controls['rows'].set_value(life.rows)
            controls['cols'].set_value(life.cols)
            update_drawing('Loaded from file: {} New size: {},{}'.format(
                f_name, life.rows, life.cols)
            )

    def onSave(self, *args):
        f_name = pick_file('Save to file', save=True)
        if f_name is not None:
            life.save(f_name)
            update_drawing('Saved to file: ' + f_name)

    def onPlay(self, *args):
        play()

    def onGridClick(self, area, event):
        flip_result = life.flip_on_click(event.x, event.y)
        if flip_result is not None:
            update_drawing('Cell {},{} flipped'.format(flip_result[0],
                                                       flip_result[1]))

    def onShapeChange(self, *args):
        rows = controls['rows'].get_value()
        cols = controls['cols'].get_value()
        life.resize(int(rows), int(cols))

        life.h_wrap = controls['h_wrap'].get_active()
        life.v_wrap = controls['v_wrap'].get_active()
        update_drawing('Grid shape changed')

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


def update_drawing(msg=''):
    status.set_text(msg)
    drawing_area.queue_draw()


def play():
    life.next_gen()
    drawing_area.queue_draw()

    if auto_button.get_active():
        t = Timer(1 / controls['speed'].get_value(), play)
        t.start()
        status.set_text('Auto playing')
    else:
        status.set_text('Idle')


def pick_file(title, save=False):
    if save:
        action = Gtk.FileChooserAction.SAVE
        btn = Gtk.STOCK_SAVE
    else:
        action = Gtk.FileChooserAction.OPEN
        btn = Gtk.STOCK_OPEN

    dialog = Gtk.FileChooserDialog(
        title=title, parent=window, action=action
    )
    dialog.add_buttons(
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        btn, Gtk.ResponseType.OK,
    )

    f_name = None
    if dialog.run() == Gtk.ResponseType.OK:
        f_name = dialog.get_filename()

    dialog.destroy()
    return f_name


if __name__ == '__main__':

    # Handle pressing Ctr+C properly, ignored by default
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    builder = Gtk.Builder()
    builder.add_from_file('life_main.glade')
    builder.connect_signals(Handler())

    window = builder.get_object('window_main')
    drawing_area = builder.get_object('drawing_area')
    status = builder.get_object('lb_status')
    auto_button = builder.get_object('bt_auto')

    ctrls_list = ['rows', 'cols', 'h_wrap', 'v_wrap', 'alive_perc',
                  'alive_nbr_min', 'alive_nbr_max',
                  'birth_nbr_min', 'birth_nbr_max',
                  'moore', 'von_neumann',
                  'speed']
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
