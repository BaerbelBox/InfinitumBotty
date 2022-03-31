import random

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from essen import essen


class GiveFoodObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".food"]

    @staticmethod
    def help():
        return ".food - gibt etwas zu essen aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.food') == -1:
            return
        connection.send_back('\001ACTION tischt ' + data['nick'] + ' ' + random.choice(essen) + ' auf.\001', data)
