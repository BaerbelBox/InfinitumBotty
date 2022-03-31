from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class PartyObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".party"]

    @staticmethod
    def help():
        return ".party - sorgt für Konfetti"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.party') == -1:
            return
        connection.send_back('\001ACTION schmeißt mit Konfetti aus buntem Esspapier um sich.\001', data)
