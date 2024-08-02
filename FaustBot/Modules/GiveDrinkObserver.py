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
        if data["message"].startswith(".drink"):
            connection.send_back(
                f"\001ACTION schenkt {data.get('nick')} {random.choice(getraenke)} ein.\001",
                data,
            )
