import sqlite3


class ScoreProvider(object):
    _CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS score (id INTEGER PRIMARY KEY, \
                    user TEXT, score INTEGER)'
    _GET_SCORE = 'SELECT id, score FROM score WHERE user = ?'
    _SAVE_OR_OVERWRITE = 'REPLACE INTO score (id, user, score) VALUES (?, ?, ?)'
    _DELETE_SCORE = 'DELETE FROM score WHERE user = ?'

    def __init__(self):
        self._database_connection = sqlite3.connect('faust_bot.db')
        cursor = self._database_connection.cursor()
        cursor.execute(ScoreProvider._CREATE_TABLE)
        self._database_connection.commit()

    def get_score(self, user: str):
        cursor = self._database_connection.cursor()
        cursor.execute(ScoreProvider._GET_SCORE, (user.lower(),))
        return cursor.fetchone()

    def save_or_replace(self, user: str, score: int):
        existing = self.get_score(user)
        _id = existing[0] if existing is not None else None
        data = (_id, user.lower(), score)
        cursor = self._database_connection.cursor()
        cursor.execute(ScoreProvider._SAVE_OR_OVERWRITE, data)
        self._database_connection.commit()

    def delete_score(self, user: str):
        cursor = self._database_connection.cursor()
        cursor.execute(ScoreProvider._DELETE_SCORE, (user.lower(),))
        self._database_connection.commit()

    def __exit__(self):
        self._database_connection.close()
