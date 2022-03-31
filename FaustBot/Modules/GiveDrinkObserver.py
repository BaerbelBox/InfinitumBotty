import random

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from getraenke import getraenke


class GiveDrinkObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".drink"]

    @staticmethod
    def help():
        return ".drink - schenkt Getränke aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.drink') == -1:
            return
        connection.send_back('\001ACTION schenkt ' + data['nick'] + ' ' + random.choice(getraenke) + ' ein.\001', data)
