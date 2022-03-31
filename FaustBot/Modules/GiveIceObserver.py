import random

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from icecreamlist import icecream


class GiveIceObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".ice"]

    @staticmethod
    def help():
        return ".ice - schenkt Eis"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.ice') == -1:
            return
        connection.send_back('\001ACTION serviert ' + data['nick'] + ' ' + random.choice(icecream) + '.\001', data)
