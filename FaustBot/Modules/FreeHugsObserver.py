import random

from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class FreeHugsObserver(PrivMsgObserverPrototype):
    hug_variants = [
        "nimmt {{nick}}{hug_adjective} in die Arme",
        "{hug_word} {{nick}}{hug_adjective}",
    ]
    possible_hugs = {
        variant.format(hug_word=word, hug_adjective=adjective)
        for variant in hug_variants
        for word in ["umarmt", "knuddelt", "drückt", "herzt"]
        for adjective in [" fest", " herzlichst", " sanft", ""]
    }
    possible_hugs = list(possible_hugs)

    @staticmethod
    def cmd():
        return [".hug"]

    @staticmethod
    def help():
        return ".hug - verteilt Umarmungen"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".hug"):
            hug_response = (random.choice(self.possible_hugs)).format(nick=data["nick"])
            connection.send_back(f"\001ACTION {hug_response}.\001", data)
