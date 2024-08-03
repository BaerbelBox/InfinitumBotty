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
        return ".ice - serviert Eis"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".ice"):
            connection.send_back(
                f"\001ACTION serviert {data['nick']} {random.choice(icecream)}.\001",
                data,
            )
