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
        if data['message'].find('.hug') == -1:
            return
        connection.send_back('\001ACTION knuddelt ' + data['nick'] + '.\001', data)
