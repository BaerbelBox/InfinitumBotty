from enum import Enum


class ModuleType(Enum):
    ON_JOIN = 'ON_JOIN'
    ON_KICK = 'ON_KICK'
    ON_LEAVE = 'ON_LEAVE'
    ON_PING = 'ON_PING'
    ON_NICK_CHANGE = 'ON_NICK_CHANGE'
    ON_MSG = 'ON_MSG'
    ON_NOTICE = 'ON_NOTICE'
    ON_MAGIC_NUMBER = 'ON_MAGIC_NUMBER'
