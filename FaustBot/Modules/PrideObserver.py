from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class PrideObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".pride"]

    @staticmethod
    def help():
        return ".party - sorgt für sehr viele Pride Flags"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.pride') == -1:
            return
        connection.send_back('\001ACTION schmückt den Channel mit ganz vielen großen Pride Flaggen.\001', data)
