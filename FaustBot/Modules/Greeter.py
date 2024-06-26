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
    greetings_dict['Luci'] = "Hewuu"
    greetings_dict['pome'] = "Hewuu"
    greetings_dict['Skadi'] = "Awoo"
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
        if data['channel'] == connection.details.get_channel():
            if data['nick'].find("Guest") != -1:
                return
            UProvider= UserProvider()
            if(UProvider.get_characters(data['nick'])) < 100:
                return
        if data['channel'] == connection.details.get_channel():
            if int(time.time()) - self.names[data['nick']] > 28800:
                if Greeter.greetings_dict[data['nick']] != "":
                    connection.send_back(Greeter.greetings_dict[data['nick']]+" " + data['nick'], data)
                else:
                    connection.send_back(self.greeting+" " + data['nick'], data)

            self.names[data['nick']] = int(time.time())