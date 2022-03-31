import datetime
import time

from FaustBot.Communication.Connection import Connection
from FaustBot.Model.UserProvider import UserProvider
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from ..Model.i18n import i18n
from FaustBot.Model.BlockedUsers import BlockProvider

class BlockObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [""]

    @staticmethod
    def help():
        return ""

    def update_on_priv_msg(self, data, connection: Connection):
        if not self._is_idented_mod(data, connection):
            return
        if data['message'].find('.block ') != -1:
            self.block(data, connection)
        if data['message'].find ('.unblock')!=-1:
            self.unblock(data, connection)
        if data['message'].find('.isblocked') != -1:
            self.isBlocked(data, connection)

    def block(self,data,connection):
        blocklist = BlockProvider()
        blocklist.block(self.isolateTarget(data))
        connection.send_back("blocked: "+ self.isolateTarget(data), data)

    def unblock(self,data,connection):
        blocklist = BlockProvider()
        blocklist.delete_block(self.isolateTarget(data))
        connection.send_back("unblocked: "+ self.isolateTarget(data), data)

    def isBlocked(self,data,connection):
        blocklist= BlockProvider()
        answ = blocklist.is_blocked(self.isolateTarget(data))
        if answ:
            connection.send_back(self.isolateTarget(data) + " ist geblocked", data)
            return
        connection.send_back(self.isolateTarget(data)+" ist nicht geblocked", data)
    def isolateTarget(self,data):
        return data['message'].split(' ')[1]

    def _is_idented_mod(self, data: dict, connection: Connection):
        return data['nick'] in self._config.mods and connection.is_idented(data['nick'])