class ConnectionDetails(object):
    def get_server(self):
        """
        :return: the server to connect to
        """
        return self._data['server']

    def get_nick(self):
        """
        :return: own nick
        """
        return self._data['nick']

    def get_channel(self):
        """
        :return: the channel connected into
        """
        return self._data['channel']

    def get_port(self):
        return int(self._data['port'])

    def get_lang(self):
        return self._data['lang']

    def change_lang(self, lang):
        self._data['lang'] = lang

    def get_mods(self):
        return self._data['mods']

    def get_pwd(self):
        if self._data['pwd'] is None:
            return ''
        return self._data['pwd']

    def __init__(self, config):
        self._data = config
