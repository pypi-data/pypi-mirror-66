import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Custom character generator")

        # {{{ Containers
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                           spacing=6)
        self.add(self.box)

        self.grid = Gtk.Grid()
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_column_spacing(2)
        self.grid.set_row_spacing(2)
        self.box.pack_start(self.grid, True, True, 0)
        # }}}

        # {{{ Bitmap
        self.bits = [[None for _ in range(0,5)] for _ in range(0,11)]
        for x in range(0,5):
            for y in range(0,11):
                bit = Gtk.CheckButton.new()
                bit.set_mode(draw_indicator = False)
                id = bit.connect("toggled", self.update)
                self.grid.attach(bit, x, y, 1, 1)
                self.bits[y][x] = (bit, id)
        # }}}

        # {{{ Representation
        self.conv_func = bin
        self.represent = Gtk.Box(spacing=6)
        self.represent.set_halign(Gtk.Align.CENTER)
        self.box.pack_start(self.represent, True, True, 0)

        self.binary = Gtk.RadioButton.new_with_label_from_widget(None, "Binary")
        self.binary.connect("toggled", self.set_represent, bin)
        self.represent.pack_start(self.binary, False, False, 0)
        self.deci = Gtk.RadioButton.new_with_label_from_widget(self.binary, "Decimal")
        self.deci.connect("toggled", self.set_represent, str)
        self.represent.pack_start(self.deci, False, False, 0)
        self.hexa = Gtk.RadioButton.new_with_label_from_widget(self.binary, "Hexadecimal")
        self.hexa.connect("toggled", self.set_represent, hex)
        self.represent.pack_start(self.hexa, False, False, 0)

        # }}}

        # {{{ Mode
        self.mode = 11
        self.modes = Gtk.Box(spacing=6)
        self.modes.set_halign(Gtk.Align.CENTER)
        self.box.pack_start(self.modes, True, True, 0)

        self.eleven_mode = Gtk.RadioButton.new_with_label_from_widget(None, "5x11")
        self.eleven_mode.connect("toggled", self.set_mode, 11)
        self.modes.pack_start(self.eleven_mode, False, False, 0)
        self.ten_mode = Gtk.RadioButton.new_with_label_from_widget(self.eleven_mode, "5x10")
        self.ten_mode.connect("toggled", self.set_mode, 10)
        self.modes.pack_start(self.ten_mode, False, False, 0)
        self.eight_mode = Gtk.RadioButton.new_with_label_from_widget(self.eleven_mode, "5x8")
        self.eight_mode.connect("toggled", self.set_mode, 8)
        self.modes.pack_start(self.eight_mode, False, False, 0)
        # }}}

        # {{{ Separator
        self.sep_box = Gtk.Box()
        self.box.pack_start(self.sep_box, True, True, 0)

        self.sep_box.pack_start(Gtk.Label(label="Separator"), True, True, 0)

        self.sep = Gtk.Entry()
        self.sep.set_text(", ")
        self.sep.connect("changed", self.update)
        self.sep_box.pack_start(self.sep, True, True, 0)
        # }}}

        # {{{ Output
        self.output = Gtk.Entry()
        self.output.set_editable(False)
        self.box.pack_start(self.output, True, True, 0)
        # }}}

        # {{{ Buttons
        self.button_box = Gtk.Box()
        self.box.pack_start(self.button_box, True, True, 0)

        self.check = Gtk.Button(label="Check all")
        self.check.connect("clicked", lambda _: self.set_bits(True))
        self.button_box.pack_start(self.check, True, True, 0)
        self.uncheck = Gtk.Button(label="Uncheck all")
        self.uncheck.connect("clicked", lambda _: self.set_bits(False))
        self.button_box.pack_start(self.uncheck, True, True, 0)
        # }}}

        self.update_mode()
        self.update()

    def set_bits(self, status):
        for line in self.bits:
            for bit, id in line:
                with bit.handler_block(id):
                    bit.set_active(status)
        self.update()

    def update_mode(self, *args):
        for i, line in enumerate(self.bits[8:11]):
            for bit, id in line:
                bit.set_visible(i+8 < self.mode)
        self.update()

    def update(self, *args):
        data = []
        for line in self.bits[:self.mode]:
            bitmap = [bit.get_active() for bit, _ in line]
            data.append(sum([int(v)<<i for i, v in enumerate(bitmap[::-1])]))
        self.output.set_text(self.sep.get_text().join([self.conv_func(x) for x in data]))

    def set_represent(self, widget, func):
        self.conv_func = func
        self.update()

    def set_mode(self, widget, mode):
        self.mode = mode
        self.update_mode()


def main():
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
