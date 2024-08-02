from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.JoinObserverPrototype import JoinObserverPrototype
from FaustBot.Model.UserProvider import UserProvider
from time import sleep


class First_Greeter(JoinObserverPrototype):
    """
    A Class only reacting to pings
    """

    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def __init__(self, greeting):
        super().__init__()
        self.first_greeting = greeting

    def update_on_join(self, data, connection: Connection):
        if data["channel"] == connection.details.get_channel():
            new_nick = data["nick"]
            if (
                new_nick.startswith("Guest")
                or UserProvider().get_characters(new_nick) < 100
            ):
                sleep(20)
                if "{NICK}" in self.first_greeting:
                    greeting = self.first_greeting.replace("{NICK}", new_nick)
                else:
                    greeting = f"{self.first_greeting} {new_nick}"
                connection.send_back(greeting, data)
