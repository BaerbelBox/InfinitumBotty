import random

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from snacks import snacks


class SnacksObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".snack"]

    @staticmethod
    def help():
        return ".snack - teilt Snacks aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".snack"):
            connection.send_back(
                f"\001ACTION serviert {data['nick']} {random.choice(snacks)}.\001", data
            )
