class Config(object):
    CONFIG_PATH = 'config_path'

    def __init__(self, path):
        """

        :param path:
        """
        self._config_dict = {}
        if path:
            self._config_dict[Config.CONFIG_PATH] = path
            self.read_config(path)

    def __getitem__(self, item: str):
        if item in self._config_dict:
            return self._config_dict[item]
        else:
            return None

    def __setitem__(self, key: str, value: str):
        print (key +' '+ value+'\n\r')
        self._config_dict[key] = value

    def read_config(self, path: str, append=True):
        f = open(path, 'r')
        if not append:
            self._config_dict = {}
        for l in f.readlines():
            kv_pair = l.split(':')
            if len(kv_pair) == 2:
                self._config_dict[kv_pair[0].strip()] = kv_pair[1][:-1].strip()
        mods = self._config_dict['mods'].split(',')
        self._config_dict['mods'] = []
        for mod in mods:
            self._config_dict['mods'].append(mod.strip())
        # If no idle_time value is given, we set it to five hours ( == 18000 seconds )
        if 'idle_time' not in self._config_dict:
            self._config_dict['idle_time'] = 18000
        self._config_dict['idle_time'] = int(self._config_dict['idle_time'])
        if 'blacklist' not in self._config_dict:
            self._config_dict['blacklist'] = []
        else:
            blacklist=self._config_dict['blacklist'].split(',')
            self._config_dict['blacklist'] =  []
            for module in blacklist:
                self._config_dict['blacklist'].append(module.strip())

    @property
    def lang(self):
        return self._config_dict["lang"]

    @lang.setter
    def lang(self, value):
        self._config_dict["lang"] = value

    @property
    def mods(self):
        return self._config_dict["mods"]

    @mods.setter
    def mods(self, value):
        self._config_dict["mods"] = value

    @property
    def idle_time(self):
        return self._config_dict["idle_time"]

    @idle_time.setter
    def idle_time(self, value: int):
        self._config_dict["idle_time"] = value

    @property
    def blacklist(self):
        return self._config_dict['blacklist']

    @property
    def pwd(self):
        return self._config_dict['pwd']