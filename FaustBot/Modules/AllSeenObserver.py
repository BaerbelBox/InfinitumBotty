import datetime
import time
from collections import defaultdict
from FaustBot.Communication.Connection import Connection
from FaustBot.Model.UserProvider import UserProvider
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from ..Model.i18n import i18n
from FaustBot.Modules.UserList import UserList

class AllSeenObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".seen"]

    @staticmethod
    def help():
        return ".seen <nick> - um abzufragen wann <nick> zuletzt hier war"

    def __init__(self, user_list: UserList):
        super().__init__()
        self.user_list = user_list

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.allseen') == -1:
            return
        if not self._is_idented_mod(data, connection):
            return
        User_afk = defaultdict(int)
        for who in self.user_list.userList.keys():
            user_provider = UserProvider()
            activity = user_provider.get_activity(who)
            delta = time.time() - activity
            User_afk[who] = delta
            print(who)
            print(delta)
        for w in sorted(User_afk, key=User_afk.get):
            output = (w+":\t"+str(datetime.timedelta(seconds=User_afk[w])))
            connection.send_back(output, data)

    def _is_idented_mod(self, data: dict, connection: Connection):
        return data['nick'] in self._config.mods and connection.is_idented(data['nick'])