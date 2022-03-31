from FaustBot.Communication.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from FaustBot.Modules.JoinObserverPrototype import JoinObserverPrototype
from FaustBot.Model.Config import Config
from enum import Enum
from datetime import datetime

"""
This Module contains multiple classes to handle spam.
Goal of this module is to provide an easy to use AntiSpam-Module, which can be activated if needed.
It should support multiple modes regarding the aggressivity of the anti-spam-handling. 
"""


class AntiSpamLevel(Enum):
    """
    Which action to be done if spam is detected.
    """
    OFF = 0  # No action is taken if spam is detected.
    WARN = 1  # Warns the user by messaging him/her without any further steps.
    WARN_KICK = 2  # Warns the user first, then kicks him/her.
    KICK = 3  # Kicks the user without any further warning.
    WARN_KICK_BAN = 4  # Like WARN_KICK but also bans the user directly.
    KICK_BAN = 5  # Like KICK, but also bans the user directly.


class AntiSpamAggressivity(Enum):
    """
    Settings to detect spam.
    a: Amount of seconds between two similiar messages to detect them as spam
    b: Amount of (non similiar) messages to be received with time-distance c, to detect them as spam
    c: Time between messages of b:
    d: Trustfactor
    """
    LOW = (3, 7, 0.5, 15)  # (a, b, c, d)
    MEDIUM = (5, 5, 0.7, 10)
    HIGH = (7, 3, 1.0, 5)
    ULTRA = (10, 3, 1.0, 2)


class AntiSpamEntry(object):
    """
    Entry collecting information about possible spammers.
    """

    def __init__():
        super().__init__()
        self.user = ""
        self.warn_count = 0
        self.msg = ""
        self.timestamp = datetime.now() 

    @property
    def user(self):
        return self.user

    @user.setter
    def user(self, user)
        self.user = user
    
    @property
    def warn_count(self):
        return self.warn_count

    @warn_count.setter
    def warn_count(self, warn_count)
        self.warn_count = warn_count

    def inc_warn_count(self)
        self.warn_count += 1

    @property
    def msg(self):
        return self.msg

    @msg.setter
    def msg(self, msg):
        self.msg = msg

    @property
    def timestamp(self):
        return self.timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self.timestamp = timestamp


class AntiSpamObserver(PrivMsgObserverPrototype, JoinObserverPrototype):

    @staticmethod
    def cmd():
        raise NotImplementedError("TBD!")

    @staticmethod
    def help():
        raise NotImplementedError("TBD!")

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_JOIN,
                ModuleType.ON_PRIVMSG]

    def __init__(self, config : Config):
        super().__init__()
        self._msg_map = dict()
        self._anti_spam_level = AntiSpamLevel.OFF
        self._anti_spam_aggressivity = AntiSpamAggressivity.LOW

    def update_on_priv_msg(self, data, connection: Connection):
        if _bot_name in  data['channel']:  # TBD! _bot_name should be fetched from the config! 
            self._handle_command(data, connection)

        if self._anti_spam_level == AntiSpamLevel.OFF:
            return

    def update_on_join(self, data: dict, connection: Connection):
        raise NotImplementedError("TBD!")

    def _is_spam(self, user: str, msg: str)
        pass

    def _handle_command(self, data: dict, connection: Connection)
        pass

    def _is_idented_mod(self, data: dict, connection: Connection):
        """
        Check wether the issuer of a module control command is a moderator or not
        """
        return data['nick'] in self._config.mods and connection.is_idented(data['nick']
