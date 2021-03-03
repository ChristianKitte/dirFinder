import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Dialog_Info(Gtk.Dialog):
    """
    A simple dialog to inform about the process of saving the current list. It pops up after
    fullfilled saving of the list.
    """

    def __init__(self, parent, title, message):
        """
        The constructor

        :param parent: The parent from which the dialog has been called
        :param title: The title
        :param message: The message
        """
        Gtk.Dialog.__init__(self, title, parent, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        self.label = Gtk.Label(message)

        self.box = self.get_content_area()
        self.box.set_spacing(6)
        self.box.set_margin_start(6)
        self.box.set_margin_end(6)
        self.box.set_margin_top(6)
        self.box.set_margin_bottom(6)

        self.box.add(self.label)
        self.show_all()
