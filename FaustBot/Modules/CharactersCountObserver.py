from FaustBot.Communication.Connection import Connection
from FaustBot.Model.UserProvider import UserProvider
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class CharactersCountObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".characters"]

    @staticmethod
    def help():
        return ".characters - um abzufragen wieviel du bisher geschrieben hast."

    def update_on_priv_msg(self, data, connection: Connection):
        if data["message"].startswith(".characters"):
            user_provider = UserProvider()
            output = f"{data['nick']}: du hast {str(user_provider.get_characters(data['nick']))} Zeichen geschrieben."
            connection.send_back(output, data)
