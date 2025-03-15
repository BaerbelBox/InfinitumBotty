from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.JoinObserverPrototype import JoinObserverPrototype
from FaustBot.Model.UserProvider import UserProvider
import time
from collections import defaultdict


class Greeter(JoinObserverPrototype):
    """
    A Class only reacting to pings
    """

    greetings_dict = defaultdict(str)
    greetings_dict["Luci"] = "Hewuu"
    greetings_dict["pome"] = "Hewuu"
    greetings_dict["Skadi"] = "Awoo {NICK}!"

    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def __init__(self, greeting):
        super().__init__()
        self.names = defaultdict(int)
        self.greeting = greeting

    def update_on_join(self, data, connection: Connection):
        if data["channel"] == connection.details.get_channel():
            joined_user = data["nick"]
            if (
                joined_user.startswith("Guest")
                or new_nick.startswith("NeuerGast")
                or UserProvider().get_characters(joined_user) < 100
            ):
                return

            if int(time.time()) - self.names[joined_user] > 28800:
                greeting_text = self.greetings_dict.get(joined_user, self.greeting)

                if "{NICK}" in greeting_text:
                    response = greeting_text.replace("{NICK}", joined_user)
                else:
                    response = f"{greeting_text} {joined_user}"
                connection.send_back(response, data)

            self.names[joined_user] = int(time.time())
