import random
import time
from collections import defaultdict

from FaustBot.Communication.Connection import Connection
from FaustBot.Model.UserProvider import UserProvider
from FaustBot.Modules.UserList import UserList
from getraenke import getraenke
from essen import essen
from icecreamlist import icecream

from ..Modules.PingObserverPrototype import PingObserverPrototype


class Kicker(PingObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def __init__(self, user_list: UserList, idle_time: int):
        super().__init__()
        self.idle_time = idle_time
        self.user_list = user_list
        self.warned_users = defaultdict(int)

    def update_on_ping(self, data, connection: Connection):
        for user in self.user_list.userList.keys():
            offline_time = Kicker.get_offline_time(user)
            if offline_time < self.idle_time:
                self.warned_users[user] = 0
            host = self.user_list.userList.get(user).host
            if offline_time > self.idle_time \
                    and not user == connection.details.get_nick() \
                    and 'freenode/staff' not in host and 'freenode/utility-bot' not in host:
                if self.warned_users[user] % 30 == 0:
                    connection.send_channel(
                        '\001ACTION serviert ' + user + ' ' + random.choice(getraenke+essen+icecream) + '.\001')
                self.warned_users[user] += 1
                if self.warned_users[user] % 29 == 0:
                    connection.raw_send("KICK " + connection.details.get_channel() + " " + user +
                                        " :Zu lang geidlet, komm gerne wieder!")

    @staticmethod
    def get_offline_time(nick):
        who = nick
        user_provider = UserProvider()
        activity = user_provider.get_activity(who)
        delta = time.time() - activity
        return delta
