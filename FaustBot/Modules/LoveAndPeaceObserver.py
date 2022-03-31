from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class LoveAndPeaceObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".peace"]

    @staticmethod
    def help():
        return ".peace - sorgt für Frieden"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.peace') == -1:
            return
        connection.send_back('\001ACTION hüpft durch den Raum, schmeißt Blumen um sich und singt: \"Love and '
                             'Peace, wir haben uns alle lieb..!\".\001', data)
