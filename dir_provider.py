from os import path
import sqlite3
from dialog_info import Dialog_Info


class DirProvider:
    """
    This class owns the pattern list. All logic for where to get the pattern from or how
    to save it goes here.

    To keep things simple the class knows about the SQLite and its rules.
    """
    __store = ''  # path to store SQLite file
    __pattern = []  # internal list of pattern

    @staticmethod
    def set_store(store):
        """
        Sets the path and initiate an refresh.
        :param store: Path to store SQLite file
        :return: Nothing
        """
        DirProvider.__store = store
        DirProvider.refresh()

    @staticmethod
    def get_pattern():
        """
        Returns a list of pattern.
        :return: A list of pattern
        """
        return DirProvider.__pattern

    @staticmethod
    def add_pattern(pattern):
        """
        Adds a new pattern to the list of pattern.
        :param pattern: A new pattern
        :return: Nothing
        """
        item_array = DirProvider.get_index(pattern)
        if len(item_array) == 0:
            DirProvider.__pattern.append(pattern)

    @staticmethod
    def remove_pattern(pattern):
        """
        Removes a patter from the list of pattern.
        :param pattern: A pattern to be removed from the list
        :return: Nothing
        """
        item_array = DirProvider.get_index(pattern)
        if len(item_array) > 0:
            DirProvider.__pattern.remove(pattern)

    @staticmethod
    def change_pattern(old_pattern, new_pattern):
        """
        Changes a patter from the list of pattern.
        :param old_pattern: The old pattern to be changed
        :param new_pattern: The new Pattern
        :return: Nothing
        """
        item_array = DirProvider.get_index(old_pattern)
        if len(item_array) > 0:
            DirProvider.__pattern[item_array[0][0]] = new_pattern

    @staticmethod
    def save():
        """
        Saves the Pattern into an SQLite database.
        :return: Nothing
        """
        if path.exists(DirProvider.__store) == True:
            try:
                connection = sqlite3.connect(DirProvider.__store)
                cursor = connection.cursor()

                sql = "delete from pattern"
                cursor.execute(sql)

                for pat in DirProvider.__pattern:
                    sql = "insert into pattern (pattern) values ('" + pat + "')"
                    cursor.execute(sql)

                connection.commit()
                connection.close()
            except Exception as err:
                print("Erro {}".format(err))

    @staticmethod
    def refresh():
        """
        Refreshes the internal list of pattern with the content of an SQLite database. If there
        is no, one will be created.
        :return: Nothing
        """
        if path.exists(DirProvider.__store) == True:
            try:
                connection = sqlite3.connect(DirProvider.__store)
                cursor = connection.cursor()

                sql = "select * from pattern order by pattern"
                cursor.execute(sql)
                result = cursor.fetchall()

                DirProvider.__pattern.clear()
                for pat in result:
                    DirProvider.__pattern.append(pat[0])

                connection.close()
            except Exception as err:
                print("Erro {}".format(err))
        else:
            DirProvider.__create_db()

    @staticmethod
    def get_index(pattern):
        """
        A helper method which returns the index of the given pattern.
        :param pattern: The pattern of which the index should be returned
        :return: The index
        """
        return [(index, text) for index, text in enumerate(DirProvider.__pattern) if text == pattern]

    @staticmethod
    def __create_db():
        """
        Creates a new SQLite database.
        :return: Nothing
        """
        if path.exists(DirProvider.__store) == False:
            try:
                connection = sqlite3.connect(DirProvider.__store)
                cursor = connection.cursor()

                sql = "CREATE TABLE pattern(pattern text not null)"
                cursor.execute(sql)

                cursor.close()
            except Exception as err:
                print("Erro {}".format(err))
