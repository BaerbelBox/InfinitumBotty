

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class TellObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.tell') != -1 and self._is_idented_mod(data, connection):
            connection.send_channel(data['messageCaseSensitive'][6:])
        if data['message'].find('.mtell') != -1 and self._is_idented_mod(data, connection):
            connection.send_channel('\001ACTION'+data['messageCaseSensitive'][7:]+'\001')
    def _is_idented_mod(self, data: dict, connection: Connection):
        return data['nick'] in self._config.mods and connection.is_idented(data['nick'])