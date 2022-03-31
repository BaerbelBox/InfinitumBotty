from FaustBot.Model.RemoteUser import RemoteUser
from FaustBot.Modules.JoinObserverPrototype import JoinObserverPrototype
from FaustBot.Modules.ModuleType import ModuleType
from ..Modules.KickObserverPrototype import KickObserverPrototype
from ..Modules.LeaveObserverPrototype import LeaveObserverPrototype
from ..Modules.NickChangeObserverPrototype import NickChangeObserverPrototype


class UserList(JoinObserverPrototype, KickObserverPrototype, LeaveObserverPrototype, NickChangeObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def __init__(self):
        super().__init__()
        self.userList = {}

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_JOIN, ModuleType.ON_KICK, ModuleType.ON_LEAVE, ModuleType.ON_NICK_CHANGE]

    def update_on_kick(self, data, connection):
        if data['nick'] in self.userList:
            del self.userList[data['nick']]
#         print(self.userList)

    def update_on_leave(self, data, connection):
        if data['nick'] in self.userList:
            del self.userList[data['nick']]
#         print(self.userList)

    def update_on_join(self, data, connection):
        self.userList[data['nick']] = RemoteUser(data['nick'], data['user'], data['host'])
#         print(self.userList)

    def update_on_nick_change(self, data, connection):
        if data['old_nick'] in self.userList:
            remuser = self.userList[data['old_nick']]
            del self.userList[data['old_nick']]
        else:
            # shouldn't happen but let's be safe.
            remuser = RemoteUser('UN.KNOWN', 'UN.KNOWN', 'UN.KNOWN')

        remuser.nick = data['new_nick']
        self.userList[data['new_nick']] = remuser
#         print(self.userList)

    def clear_list(self):
        self.userList = {}

    def add_user(self, remuser):
        self.userList[remuser.nick] = remuser
