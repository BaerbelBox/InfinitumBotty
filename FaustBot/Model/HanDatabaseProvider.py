import sqlite3


class HanDatabaseProvider(object):
    _CREATE_HANDB_TABLE = 'CREATE TABLE IF NOT EXISTS handb (id INTEGER PRIMARY KEY, \
                                hanword TEXT)'
    _GET_RANDOM_WORD = 'SELECT hanword FROM handb ORDER BY RANDOM() LIMIT 1'
    _INSERT_WORD = 'REPLACE INTO handb(id, hanword) VALUES (?,?)'
    _DELETE_WORD = 'DELETE FROM handb WHERE hanword = ?'
    _GET_WORD = 'SELECT id, hanword FROM handb WHERE hanword = ?'
    def __init__(self):
        self._database_connection = sqlite3.connect('faust_bot.db')
        cursor = self._database_connection.cursor()
        cursor.execute(HanDatabaseProvider._CREATE_HANDB_TABLE)
        self._database_connection.commit()

    def get_random_word(self):
        """

        :param abbreviation:
        :return:
        """
        cursor = self._database_connection.cursor()
        cursor.execute(HanDatabaseProvider._GET_RANDOM_WORD)
        return cursor.fetchone()

    def get_hanWord(self, HanWord):
        """

        :param abbreviation:
        :return:
        """
        cursor = self._database_connection.cursor()
        cursor.execute(HanDatabaseProvider._GET_WORD, (HanWord.upper(),))
        return cursor.fetchone()

    def addWord(self, HanWord):
        """

        :param abbreviation:
        :param explanation:
        :return:
        """
        existing = self.get_hanWord(HanWord)
        _id = existing[0] if existing is not None else None
        data = (_id, HanWord)
        cursor = self._database_connection.cursor()
        cursor.execute(HanDatabaseProvider._INSERT_WORD, data)
        self._database_connection.commit()

    def delete_hanWord(self, HanWord):
        cursor = self._database_connection.cursor()
        cursor.execute(HanDatabaseProvider._DELETE_WORD, (HanWord.strip(),))
        self._database_connection.commit()

    def __exit__(self, exc_type, exc_value, traceback):
        self._database_connection.close()
