import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import sys

class SimpleNotepad(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Notepad")
        self.set_default_size(600, 400)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.textview)

        button_save = Gtk.Button(label="Сохранить")
        button_save.connect("clicked", self.on_save_clicked)

        button_open = Gtk.Button(label="Открыть")
        button_open.connect("clicked", self.on_open_clicked)

        button_print = Gtk.Button(label="Печать")
        button_print.connect("clicked", self.on_print_clicked)

        button_test = Gtk.Button(label="Keyboard Test")
        button_test.connect("clicked", self.on_test_clicked)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_homogeneous(False)
        vbox.pack_start(scrolled_window, True, True, 0)

        hbox1 = Gtk.Box(spacing=10)
        hbox1.set_homogeneous(False)
        hbox1.pack_start(button_save, True, True, 0)
        hbox1.pack_start(button_open, True, True, 0)
        hbox1.pack_start(button_print, True, True, 0)

        hbox2 = Gtk.Box(spacing=10)
        hbox2.set_homogeneous(False)
        hbox2.pack_start(button_test, True, True, 0)

        vbox.pack_end(hbox1, False, True, 0)
        vbox.pack_end(hbox2, False, True, 0)

        self.add(vbox)

    def on_save_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Сохранить файл", self, Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            start, end = self.textbuffer.get_bounds()
            text = self.textbuffer.get_text(start, end, True)
            with open(filename, 'w') as file:
                file.write(text)
        dialog.destroy()

    def on_open_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Открыть файл", self, Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        dialog.set_select_multiple(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filenames = dialog.get_filenames()
            for filename in filenames:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                    text = file.read()
                    self.textbuffer.set_text(text)
        dialog.destroy()

    def on_print_clicked(self, widget):
        settings = Gtk.PrintSettings()
        print_operation = Gtk.PrintOperation()

        def print_text(operation, context, page_nr):
            start, end = self.textbuffer.get_bounds()
            text = self.textbuffer.get_text(start, end, False)
            context.set_font_name("Monospace 12")
            context.set_text(text)

        print_operation.connect("draw-page", print_text)
        print_operation.set_default_page_setup(settings.get_default_page_setup())
        result = print_operation.run(Gtk.PrintOperationAction.PRINT_DIALOG, None)

        if result == Gtk.PrintOperationResult.ERROR:
            print("Ошибка печати")

    def on_test_clicked(self, widget):
        test_text = ("Test word " * 10 + "\n") * 5
        test_window = TestWindow(test_text)

class TestWindow(Gtk.Window):

    def __init__(self, test_text):
        Gtk.Window.__init__(self, title="Keyboard Test")
        self.set_default_size(800, 600)

        label = Gtk.Label()
        label.set_text(test_text)
        label.set_selectable(True)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(label)

        button_ok = Gtk.Button(label="OK")
        button_ok.connect("clicked", self.on_ok_clicked)

        button_cancel = Gtk.Button(label="Cancel")
        button_cancel.connect("clicked", self.on_cancel_clicked)

        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False)
        hbox.pack_start(button_ok, True, True, 0)
        hbox.pack_start(button_cancel, True, True, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_homogeneous(False)
        vbox.pack_start(scrolled_window, True, True, 0)
        vbox.pack_end(hbox, False, True, 0)

        self.add(vbox)

    def on_ok_clicked(self, widget):
        Gtk.main_quit()

    def on_cancel_clicked(self, widget):
        Gtk.main_quit()

win = SimpleNotepad()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
