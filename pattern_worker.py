import os
import subprocess
import sys
from threading import Thread


class Worker(Thread):
    """
    A small routine to iterate a list of pattern and validate it as directories  based an a search pattern.

    It's possible to open an explorer in case of successs for each directory. Further on it's possible to
    call an method in this case.

    In the end it's possible to return a list by providing another callback  method.
    """

    def __init__(self, search_templates, search_pattern, directories=[], open=True, print_out=None, print_list=None):
        """
        The constructor.
        :param search_templates: The templates
        :param search_pattern: The search pattern
        :param directories:(optional) An list to add the valid paths (content will not be cleared)
        :param open:(optional) True, if an explorer should start for each valid path
        :param print_out:(optional) A function to be called for every valid path
        :param print_list:(optional) A function to be called after a search
        """
        Thread.__init__(self)

        self.search_templates = search_templates
        self.search_pattern = search_pattern
        self.directories = directories
        self.open = open
        self.print_out = print_out
        self.print_list = print_list

    def run(self):
        """
        For each pattern within the list of patterns a string will be created by the pattern and the given
        search string. Afterwards it will be checked if the strings represents a valid path.

        For each valid path a new explorer will be opened (if open equals true). If a function is defined
        it will be called.

        If defined a function will be called afterwards.
        :return: nothing
        """
        for search_string in (p.format(pattern=self.search_pattern) for p in self.search_templates):
            exist = os.path.exists(search_string)
            if exist:
                self.directories.append(search_string)
                if self.print_out: self.print_out(search_string)

                if open:
                    # os.startfile(search_string)

                    try:
                        # https://www.deruli.de/?single=python-osstartfile-nicht-nur-fuer-windows
                        # Windows
                        if os.name == "nt":
                            os.startfile(search_string)
                        # Macintosh
                        elif sys.platform == "darwin":
                            subprocess.call(['open', search_string])
                        # Generisches Unix (X11)
                        else:
                            subprocess.call(['xdg-open', search_string])
                    except Exception as err:
                        print("Erro {}".format(err))

        if self.print_list: self.print_list(self.directories)
