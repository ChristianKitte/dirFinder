"""
Solution EA2: dirFinder (Gtk+)

An application which searches for existing directories. For each directory a explorer will be opened.

For this a list of pattern can be provided by the user. Each with a part like "{pattern}". This very
one part will be replaced be s search String given by the user.

Anyway each pattern as descriped above will be handelt as a valid directory an as this being verified.
If exist, an explorer will be called.

"c:\a\b\{pattern}"  ==> with "180045"  goes to "c:\a\b\180045"

__version__ = '1.0'
__author__ = 'Christian Kitte'

"""
if __name__ == "__main__":
    import gi

    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk

    from dir_provider import DirProvider
    from main_form import MainWindow
    from os import path
    from os import curdir

    DirProvider.set_store(path.abspath(curdir) + 'store')

    win = MainWindow()

    pixbuf = Gtk.IconTheme.get_default().load_icon("edit-find", 64, 0)
    win.set_icon(pixbuf)

    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
