import sqlite3


class GlossaryProvider(object):
    _CREATE_GLOSSARY_TABLE = 'CREATE TABLE IF NOT EXISTS glossary (id INTEGER PRIMARY KEY, \
                                abbreviation TEXT, explanation TEXT)'
    _GET_EXPLANATION = 'SELECT id, explanation FROM glossary WHERE abbreviation = ?'
    _SAVE_OR_OVERWRITE = 'REPLACE INTO glossary (id, abbreviation, explanation) VALUES (?, ?, ?)'
    _DELETE_EXPLANATION = 'DELETE FROM glossary WHERE abbreviation = ?'

    def __init__(self):
        self._database_connection = sqlite3.connect('faust_bot.db')
        cursor = self._database_connection.cursor()
        cursor.execute(GlossaryProvider._CREATE_GLOSSARY_TABLE)
        self._database_connection.commit()

    def get_explanation(self, abbreviation: str):
        """
        
        :param abbreviation: 
        :return: 
        """
        cursor = self._database_connection.cursor()
        cursor.execute(GlossaryProvider._GET_EXPLANATION, (abbreviation.lower(),))
        return cursor.fetchone()

    def save_or_replace(self, abbreviation: str, explanation: str):
        """
        
        :param abbreviation: 
        :param explanation: 
        :return: 
        """
        existing = self.get_explanation(abbreviation)
        _id = existing[0] if existing is not None else None
        data = (_id, abbreviation.lower(), explanation)
        cursor = self._database_connection.cursor()
        cursor.execute(GlossaryProvider._SAVE_OR_OVERWRITE, data)
        self._database_connection.commit()

    def delete_explanation(self, abbreviation: str):
        cursor = self._database_connection.cursor()
        cursor.execute(GlossaryProvider._DELETE_EXPLANATION, (abbreviation.strip(),))
        self._database_connection.commit()

    def __exit__(self, exc_type, exc_value, traceback):
        self._database_connection.close()
