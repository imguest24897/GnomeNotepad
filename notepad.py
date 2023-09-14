import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class SimpleNotepad(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Notepad")
        self.set_default_size(600, 400)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.textview)

        button_save = Gtk.Button(label="Save")
        button_save.connect("clicked", self.on_save_clicked)

        button_open = Gtk.Button(label="Open")
        button_open.connect("clicked", self.on_open_clicked)

        button_print = Gtk.Button(label="Print")
        button_print.connect("clicked", self.on_print_clicked)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_homogeneous(False)
        vbox.pack_start(scrolled_window, True, True, 0)

        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False)
        hbox.pack_start(button_save, True, True, 0)
        hbox.pack_start(button_open, True, True, 0)
        hbox.pack_start(button_print, True, True, 0)

        vbox.pack_end(hbox, False, True, 0)

        self.add(vbox)

    def on_save_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Save file", self, Gtk.FileChooserAction.SAVE,
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
        dialog = Gtk.FileChooserDialog("Open file", self, Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            with open(filename, 'r') as file:
                text = file.read()
                self.textbuffer.set_text(text)
        dialog.destroy()

    def on_print_clicked(self, widget):
        settings = Gtk.PrintSettings()
        print_operation = Gtk.PrintOperation()

        def print_text(operation, context, page_nr):
            start, end = self.textbuffer.get_bounds()
            text = self.textbuffer.get_text(start, end, True)
            context.set_font_name("Monospace 12")
            context.set_text(text)

        print_operation.connect("draw-page", print_text)
        print_operation.set_default_page_setup(settings.get_default_page_setup())
        result = print_operation.run(Gtk.PrintOperationAction.PRINT_DIALOG, None)

        if result == Gtk.PrintOperationResult.ERROR:
            print("Ошибка печати")

win = SimpleNotepad()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

