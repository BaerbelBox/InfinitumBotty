from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.JoinObserverPrototype import JoinObserverPrototype
import time
from collections import defaultdict

class Greeter(JoinObserverPrototype):
    """
    A Class only reacting to pings
    """

    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def __init__(self):
        super().__init__()
        self.names = defaultdict(int)

    def update_on_join(self, data, connection: Connection):
        if data['channel'] == connection.details.get_channel():
            if int(time.time()) - self.names[data['nick']] > 28800:
                if data['nick'].find("Neuling") != -1:
                    connection.send_back("Herzlich Willkommen bei uns "+data['nick'],data)
                    self.names[data['nick']] = int(time.time())
                    return
                connection.send_back("Hallo " + data['nick'], data)
                self.names[data['nick']] = int(time.time())