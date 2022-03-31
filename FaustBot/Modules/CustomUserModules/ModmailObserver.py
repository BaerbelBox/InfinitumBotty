from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class ModmailObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".modmail"]

    @staticmethod
    def help():
        return ".modmail <msg> - Sendet allen Moderatoren <msg> per PN"

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.modmail') == -1:
            return
        mods = connection.details.get_mods()
        print(mods)
        message = data['message'].split('.modmail ')[1]
        for mod in mods:
            connection.send_to_user(mod, data['nick'] + ' meldet: ' + message)
