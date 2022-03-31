import sqlite3


class i18n(object):
    def get_text(self, name, replacements=None, lang='de-DE'):
        """

        :param replacements:
        :param name: name of text
        :param lang: language to get text in
        :return: the text
        """
        if replacements is None:
            replacements = {}
        database_connection = sqlite3.connect('faust_bot.db')
        cursor = database_connection.cursor()
        ltext = ""
        print(replacements)
        for longText in cursor.execute("SELECT longText FROM i18n WHERE lang = ? AND ident = ?", (lang, name,)):
            ltext = longText[0]
        for (key, value) in replacements.items():
            ltext = ltext.replace('$' + key, value)
        return ltext
