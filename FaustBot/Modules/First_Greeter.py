from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.JoinObserverPrototype import JoinObserverPrototype
import time
from collections import defaultdict
from FaustBot.Model.UserProvider import UserProvider

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
        if data['channel'] == connection.details.get_channel():
            UProvider= UserProvider()
            if(UProvider.get_characters(data['nick'])) < 100:
                connection.send_back(self.first_greeting + " " + data['nick'], data)