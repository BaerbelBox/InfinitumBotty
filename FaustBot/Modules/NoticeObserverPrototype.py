from FaustBot.Communication import Connection
from FaustBot.Modules.ModulePrototype import ModulePrototype
from FaustBot.Modules.ModuleType import ModuleType


class NoticeObserverPrototype(ModulePrototype):
    @staticmethod
    def cmd():
        raise NotImplementedError()

    @staticmethod
    def help():
        raise NotImplementedError("Need sto be implemented by subclasses!")

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_NOTICE]

    def __init__(self):
        super().__init__()

    def update_on_notice(self, data, connection: Connection):
        raise NotImplementedError('Needs to be implemented by csubclasses!')
