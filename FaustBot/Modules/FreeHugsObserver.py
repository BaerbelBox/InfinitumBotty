import random

from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class FreeHugsObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".hug"]

    @staticmethod
    def help():
        return ".hug - verteilt Umarmungen"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".hug"):
            hug_word = random.choice(["umarmt", "knuddelt", "drückt", "herzt"])
            connection.send_back(f"\001ACTION {hug_word} {data['nick']}.\001", data)
