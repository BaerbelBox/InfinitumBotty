import random

from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from kekse import kekse


class GiveCookieObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".cookie"]

    @staticmethod
    def help():
        return ".cookie - verteilt Kekse; oder auch nicht"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.cookie') == -1:
            return
        connection.send_back('\001ACTION schenkt ' + data['nick'] + ' ' + random.choice(kekse) + '.\001', data)
