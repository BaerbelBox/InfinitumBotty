from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PingObserverPrototype import PingObserverPrototype


class ModulePing(PingObserverPrototype):
    """
    A Class only reacting to pings
    """

    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def update_on_ping(self, data, connection: Connection):
        # print('Module Ping')
        msg = 'PONG ' + data['server']
        connection.raw_send(msg)
