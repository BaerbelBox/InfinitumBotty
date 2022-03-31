# from ..FaustBot import ModuleType
from FaustBot.Communication.Connection import Connection
from FaustBot.Model.UserProvider import UserProvider
from FaustBot.Modules.JoinObserverPrototype import JoinObserverPrototype
from FaustBot.Modules.ModuleType import ModuleType
from ..Modules.NickChangeObserverPrototype import NickChangeObserverPrototype
from ..Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class ActivityObserver(PrivMsgObserverPrototype, JoinObserverPrototype, NickChangeObserverPrototype):
    """
    A Class only reacting to pings
    """

    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def update_on_join(self, data, connection: Connection):
        users = UserProvider()
        if data['channel'] == connection.details.get_channel():
            users.set_active(data['nick'])

    def update_on_priv_msg(self, data, connection: Connection):
        users = UserProvider()
        if data['channel'] == connection.details.get_channel():
            users.set_active(data['nick'])
            users.add_characters(data['nick'], len(data['message']))

    def update_on_nick_change(self, data, connection: Connection):
        users = UserProvider()
        users.set_active(data['new_nick'])

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_MSG, ModuleType.ON_JOIN, ModuleType.ON_NICK_CHANGE]
