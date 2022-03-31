import sqlite3


class BlockProvider(object):
    _CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS blockedusers (id INTEGER PRIMARY KEY, \
                    user TEXT)'
    _IS_BLOCKED = 'SELECT user FROM blockedusers'
    _BLOCK = 'INSERT INTO blockedusers (id, user) VALUES (?, ?)'
    _DELETE_BLOCK = 'DELETE FROM blockedusers WHERE user = ?'

    def __init__(self):
        self._database_connection = sqlite3.connect('faust_bot.db')
        cursor = self._database_connection.cursor()
        cursor.execute(BlockProvider._CREATE_TABLE)
        self._database_connection.commit()

    def is_blocked(self, user: str):
        cursor = self._database_connection.cursor()
        cursor.execute(BlockProvider._IS_BLOCKED)
        answer = cursor.fetchall()
        for ans in answer:
            if user.lower().find(ans[0])!=-1:
                return True
        return False

    def block(self, user: str):
        data = (None, user.lower())
        cursor = self._database_connection.cursor()
        cursor.execute(BlockProvider._BLOCK, data)
        self._database_connection.commit()

    def delete_block(self, user: str):
        cursor = self._database_connection.cursor()
        cursor.execute(BlockProvider._DELETE_BLOCK, (user.lower(),))
        self._database_connection.commit()

    def __exit__(self):
        self._database_connection.close()
