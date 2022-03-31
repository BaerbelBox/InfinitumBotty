class ModulePrototype(object):
    @staticmethod
    def cmd():
        raise NotImplementedError()

    @staticmethod
    def get_module_types():
        raise NotImplementedError("This method needs to be implemented by a subclass!")

    @staticmethod
    def help():
        raise NotImplementedError("Needs to be implemented by subclasses")

    def __init__(self):
        self._config = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value
