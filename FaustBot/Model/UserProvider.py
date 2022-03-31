import sqlite3
import time


class UserProvider(object):
    """
    Provides information about the users
    """

    def __init__(self):
        self.database_connection = sqlite3.connect('faust_bot.db')
        cursor = self.database_connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (id INTEGER  PRIMARY KEY , name TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_stats(id INTEGER  PRIMARY KEY, characters INT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS last_seen (id INTEGER  PRIMARY KEY, last_seen REAL)''')
        self.database_connection.commit()

    def get_characters(self, name):
        """

        :param name: name of user whom characters are to get
        :return: total number of characters written
        """
        cursor = self.database_connection.cursor()
        id = self._get_id(name)
        if id is None:
            return 0
        for characters in cursor.execute("SELECT characters FROM user_stats WHERE id = ?", (id,)):
            return characters[0]
        return 0

    def get_activity(self, name):
        """

        :param name: name of user whom activity to get
        :return: last activity by user
        """
        cursor = self.database_connection.cursor()
        id = self._get_id(name)
        if id is None:
            return 0
        for time in cursor.execute("SELECT last_seen FROM last_seen WHERE id = ?", (id,)):
            return time[0]
        return 0

    def add_characters(self, name, number):
        """

        :param name: User to Add Characters to
        :param number: Number of Characters to add
        :return: nothing
        """
        cursor = self.database_connection.cursor()
        id = self._get_id(name)
        if id is None:
            self._create_user(name)
            id = self._get_id(name)
        for chars in cursor.execute("SELECT characters FROM user_stats WHERE id = ?", (id,)):
            chars = chars[0]
            chars += number
            cursor.execute("UPDATE user_stats SET characters = ? WHERE id = ?", (chars, id,))
            self.database_connection.commit()
        return None

    def set_active(self, name):
        """

        :param name: set this user active at the moment
        :return: Nothing
        """
        cursor = self.database_connection.cursor()
        id = self._get_id(name)
        ntime = time.time()
        if id is None:
            self._create_user(name)
            id = self._get_id(name)
        cursor.execute("UPDATE last_seen SET last_seen = ? WHERE id = ?", (ntime, id,))
        self.database_connection.commit()

    def permission(self, user, percent):
        """

        :param user: user to ask permission for
        :param percent: percent needed for permission
        :return: True or False
        http://stackoverflow.com/questions/1682920/determine-if-a-user-is-idented-on-irc
        """
        return True

    def _get_id(self, name):
        cursor = self.database_connection.cursor()
        try:
            for id in cursor.execute("SELECT id FROM user WHERE name = ?", (name,)):
                return id[0]
        except:
            return None

    def _create_user(self, name):
        cursor = self.database_connection.cursor()
        cursor.execute("INSERT INTO user(name) VALUES (?)", (name,))
        id = self._get_id(name)
        cursor.execute("INSERT INTO user_stats(id, characters) VALUES (?, 0)", (id,))
        cursor.execute("INSERT INTO last_seen (id, last_seen) VALUES (?, 0)", (id,))
        self.database_connection.commit()

    def __exit__(self, exc_type, exc_value, traceback):
        self.database_connection.close()
