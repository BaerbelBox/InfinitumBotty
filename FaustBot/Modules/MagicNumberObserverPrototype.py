from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.ModulePrototype import ModulePrototype
from FaustBot.Modules.ModuleType import ModuleType


class MagicNumberObserverPrototype(ModulePrototype):
    """
    The Prototype of a Class who can react to server actions
    """

    @staticmethod
    def cmd():
        raise NotImplementedError()

    @staticmethod
    def help():
        raise NotImplementedError("Need sto be implemented by subclasses!")

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_MAGIC_NUMBER]

    def __init__(self):
        super().__init__()

    def update_on_magic_number(self, data, connection: Connection):
        raise NotImplementedError("Some module doesn't do anything")
