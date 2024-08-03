import datetime

from FaustBot.Communication.Connection import Connection
from FaustBot.Model.UserProvider import UserProvider
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class SeenObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".seen"]

    @staticmethod
    def help():
        return ".seen <nick> - um abzufragen wann <nick> zuletzt hier war"

    def update_on_priv_msg(self, data, connection: Connection):
        if data["message"].startswith(".seen ") and self._is_idented_mod(
            data, connection
        ):
            who = data["message"].split(" ")[1]

            user_provider = UserProvider()
            activity = user_provider.get_activity(who)
            if activity == 0:
                output = f"{data['nick']}: Ich habe {who} noch nicht gesehen."
            else:
                output = f"{data['nick']}: Ich habe {who} zuletzt am {str(datetime.datetime.fromtimestamp(activity).strftime('%d.%m.%Y um %H:%M:%S'))} Uhr gesehen."

            connection.send_back(output, data)

    def _is_idented_mod(self, data: dict, connection: Connection):
        return data["nick"] in self._config.mods and connection.is_idented(data["nick"])
