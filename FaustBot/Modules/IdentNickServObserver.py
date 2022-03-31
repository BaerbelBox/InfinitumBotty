import re

from FaustBot.Communication import Connection
from FaustBot.Modules.NoticeObserverPrototype import NoticeObserverPrototype


class IdentNickServObserver(NoticeObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def update_on_notice(self, data, connection: Connection):
        # b':NickServ!NickServ@services. NOTICE FaustBotDev :corvidae ACC 3 \r\n'
        if not data['nick'].lower() == 'nickserv':
            return
        with connection.condition_lock:
            if re.match(r'.*? ACC [0-3].*', data['message']):
                msg_parts = data['message'].split(' ')
                if msg_parts[2] == '3':
                    connection.idented_look_up[msg_parts[0]] = True
                else:
                    connection.idented_look_up[msg_parts[0]] = False
                connection.condition_lock.notify_all()
