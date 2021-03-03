from dir_provider import DirProvider
from dialog_info import Dialog_Info
from pattern_worker import Worker
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


class MainWindow(Gtk.Window):
    """
    The main window of the application.

    - ENTER within list activates the editfield for the current selected pattern and set the focus to it.
    - ENTER within the editfield adds the current text as a new pattern into the list. (For remove and
        change the buttons have to be clicked).
    - ARROW UP sets the focus back to the list. (ARROW UP and DOWN will be available).
    """

    def __init__(self):
        """
        The contructor.

        Based to the knowledge that within python the __ini__ method will be called AFTER the initiciation, it
        doesn't seam to be neccasarry to extract the code of creating the window itself.
        """
        Gtk.Window.__init__(self, title="dirFinder")

        self.set_default_size(150, 100)
        self.__current_selection = None

        # PAGE1
        self.hbox1 = Gtk.HBox()
        self.hbox1.set_spacing(6)
        self.hbox1.set_margin_start(6)
        self.hbox1.set_margin_end(6)
        self.hbox1.set_margin_top(6)
        self.hbox1.set_margin_bottom(6)

        self.txt_search = Gtk.Entry()
        self.txt_search.connect('key-press-event', self.on_txt_search_clicked)
        self.hbox1.pack_start(self.txt_search, False, False, 0)

        self.btn_search = Gtk.Button()
        self.btn_search.set_label('Ausführen')
        self.btn_search.connect('clicked', self.on_btn_search_clicked)
        self.hbox1.pack_start(self.btn_search, False, False, 0)

        self.page1_vbox = Gtk.VBox()
        self.page1_vbox.pack_start(self.hbox1, False, False, 0)

        # PAGE2
        self.pattern_store = self.get_list_store()
        self.treePattern = Gtk.TreeView(self.pattern_store)
        # when a row is selected, it emits a signal
        self.treePattern.get_selection().connect("changed", self.on_tree_event)
        self.treePattern.connect('key-press-event', self.on_keypress)

        self.columnPattern = Gtk.TreeViewColumn("Pattern", Gtk.CellRendererText(), text=0)
        self.treePattern.append_column(self.columnPattern)

        self.txt_editPattern = Gtk.Entry()
        self.txt_editPattern.connect('key-press-event', self.on_keypress)

        self.btn_save = Gtk.Button()
        self.btn_save.set_label('Speichern')
        self.btn_save.connect('clicked', self.on_btn_save_clicked)

        self.btn_add = Gtk.Button()
        self.btn_add.set_label('Hinzufügen')
        self.btn_add.connect('clicked', self.on_btn_add_clicked)

        self.btn_remove = Gtk.Button()
        self.btn_remove.set_label('Entfernen')
        self.btn_remove.connect('clicked', self.on_btn_remove_clicked)

        self.btn_change = Gtk.Button()
        self.btn_change.set_label('Ändern')
        self.btn_change.connect('clicked', self.on_btn_change_clicked)

        self.editButtonBox = Gtk.HBox()
        self.editButtonBox.add(self.btn_save)
        self.editButtonBox.add(self.txt_editPattern)
        self.editButtonBox.add(self.btn_add)
        self.editButtonBox.add(self.btn_remove)
        self.editButtonBox.add(self.btn_change)

        self.page2_vbox = Gtk.VBox()
        self.page2_vbox.pack_start(self.treePattern, False, False, 0)
        self.page2_vbox.pack_end(self.editButtonBox, False, False, 0)

        # NOTEBOOK
        self.nb = Gtk.Notebook()
        self.nb.append_page(self.page1_vbox, Gtk.Label('Programm'))
        self.nb.append_page(self.page2_vbox, Gtk.Label('Einstellung'))

        # MAIN WINDOW
        self.add(self.nb)
        self.set_focus(self.txt_search)

    # Handler Page1
    def on_btn_search_clicked(self, widget):
        """
        Handles clicked event for the search field (Page 1).
        :param widget: The widget
        :return: Nothing
        """
        self.start_search()

    def on_txt_search_clicked(self, widget, event):
        """
        Handles key press event specially for the search field (Page 1).
        ENTER = 65293

        :param widget: The widget
        :param event: The signal
        :return: Nothing
        """
        if event.keyval == 65293:
            self.start_search()

    # Handler Page2
    def on_keypress(self, widget, event):
        """
        Handles all key press events.
        ENTER = 65293, DEL=65535, TAB=65289, ARROW UP=65362, ARROW DOWN=65364

        :param widget: The widget
        :param event: The signal
        :return: Nothing
        """

        # daran denken: in Python and or etc. und nicht && || etc.
        if event.keyval == 65293:
            if widget == self.treePattern:
                self.update_txt_search()
                self.set_focus(self.txt_editPattern)
            else:
                self.add_pattern()
                self.update_txt_search()
                self.set_focus(self.txt_editPattern)
        elif event.keyval == 65535:
            if widget == self.treePattern:
                self.remove_pattern()
                self.update_txt_search()
                self.set_focus(self.txt_editPattern)
        elif event.keyval == 65289:
            if widget == self.treePattern:
                self.update_txt_search()
                self.set_focus(self.txt_editPattern)
        elif widget != self.treePattern and (event.keyval == 65362 or event.keyval == 65364):
            if self.treePattern.has_focus == False:
                self.set_focus(self.treePattern)
        else:
            if widget == self.treePattern and (event.keyval != 65362 and event.keyval != 65364):
                self.treePattern.emit_stop_by_name('key-press-event')

    def on_btn_save_clicked(self, widget):
        """
        Saves all the changes made to the list.
        :param widget: The widget
        :return: Nothing
        """
        self.save_pattern()

        dlgSave = Dialog_Info(self, "Gespeichert", "Die Einträge wurden gespeichert")
        dlgSave.run()
        dlgSave.destroy()

        self.set_focus(self.txt_editPattern)

    def on_btn_add_clicked(self, widget):
        """
        Adds a new listitem with the current entry of the textfield.
        :param widget: The widget
        :return: Nothing
        """
        self.add_pattern()
        self.update_txt_search()
        self.set_focus(self.txt_editPattern)

    def on_btn_remove_clicked(self, widget):
        """
        Removes the current listitem.
        :param widget: The widget
        :return: Nothing
        """
        self.remove_pattern()
        self.update_txt_search()
        self.set_focus(self.txt_editPattern)

    def on_btn_change_clicked(self, widget):
        """
        Updates the current listitem with the current entry of the textfield.
        :param widget: The widget
        :return: Nothing
        """
        if self.__current_selection != None:
            (model, iter) = self.__current_selection
            if iter is not None:
                DirProvider.change_pattern(model[iter][0], self.txt_editPattern.get_text())
                model[iter][0] = self.txt_editPattern.get_text()

        self.update_txt_search()
        self.set_focus(self.txt_editPattern)

    def on_tree_event(self, selection):
        """
        Updates the searchfield with the current list item.
        Sets __currentselection.
        :param selection: The selection
        :return: Nothing
        """
        if len(self.pattern_store) != 0:
            # get the model and the iterator that points at the data in the model
            (model, iter) = selection.get_selected()
            self.txt_editPattern.set_text(model[iter][0])
            self.__current_selection = selection.get_selected()

    # other
    def get_list_store(self):
        """
        Updates the list with the current patternlist.
        :return: Nothing
        """
        store = Gtk.ListStore(str)

        for pat in DirProvider.get_pattern():
            store.append([pat])

        return store

    def update_txt_search(self):
        """
        An helpermethod to updates the searchfield with the current list item on the fly.
        Using __currentselection.
        :return: Nothing
        """
        if self.__current_selection != None:
            (model, iter) = self.__current_selection
            if iter is not None:
                self.txt_editPattern.set_text(model[iter][0])

    def start_search(self):
        """
        Runs a search as descriped above.
        :return: Nothing
        """

        def print_entry(s):
            pass
            # print(s)

        def print_diretories(dirs):
            self.iconify()

            if len(dirs) == 0:
                print("...keine Einträge")
            else:
                for item in dirs:
                    print(item)

        try:
            m = Worker(DirProvider.get_pattern(), self.txt_search.get_text(), [], True, print_entry, print_diretories)
            m.start()
        except Exception as err:
            print("Erro {}".format(err))

    def remove_pattern(self):
        """
        Removes a patter from the list of pattern.
        :return: Nothing
        """
        if self.__current_selection != None:
            (model, iter) = self.__current_selection
            if iter is not None:
                DirProvider.remove_pattern(model[iter][0])
                self.pattern_store.remove(iter)

    def add_pattern(self):
        """
        Adds a new pattern to the list of pattern.
        :return: Nothing
        """
        item_array = DirProvider.get_index(self.txt_editPattern.get_text())
        if len(item_array) == 0:
            DirProvider.add_pattern(self.txt_editPattern.get_text())
            self.pattern_store.append([self.txt_editPattern.get_text()])

    def save_pattern(self):
        """
        Saves the Pattern into an SQLite database.
        :return: Nothing
        """
        DirProvider.save()
