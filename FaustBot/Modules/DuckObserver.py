from FaustBot.Modules.ModuleType import ModuleType
from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from FaustBot.Modules.PingObserverPrototype import PingObserverPrototype
from random import randint
from FaustBot.Model.DuckProvider import DucksProvider

class DuckObserver(PrivMsgObserverPrototype, PingObserverPrototype):
    @staticmethod
    def cmd():
        return ['.freunde', '.schiessen', '.starthunt','.stophunt','.ducks']

    @staticmethod
    def help():
        return 'duck game'

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_MSG, ModuleType.ON_PING]

    def __init__(self):
        super().__init__()
        self.active = 0
        self.duck_alive = 0

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.starthunt') != -1:
            if not self._is_idented_mod(data, connection):
                connection.send_back("Dir fehlen leider die Rechte zum Starten der Jagd, " + data['nick'] + ".",data)
                return
            self.active = 1
            connection.send_channel("Jagd eröffnet")
            return
        if data['message'].find('.stophunt') != -1:
            if not self._is_idented_mod(data, connection):
                connection.send_back("Dir fehlen leider die Rechte zum Stoppen der Jagd, " + data['nick'] + ".",
                                     data)
                return
            self.active = 0
            self.duck_alive = 0
            connection.send_channel("Jagd beendet")
            return
        if data['message'].find('.ducks') != -1:
            connection.send_channel(self.build_duck_string(data['nick']))
        if data['message'].find('.freunde') != -1:
            self.befriend(data, connection)
        if data['message'].find('.schiessen') != -1:
            self.shoot(data, connection)

    def befriend(self, data, connection):
        if self.duck_alive == 1:
            if randint(1, 100) > 97:
                connection.send_channel(data['nick'] + " probiert eine Ente zu befreunden aber sie will nicht.")
            else:
                self.duck_alive = 0
                self.addLivingDuck(data['nick'])
                connection.send_channel(self.build_duck_string(data['nick']))
            return
        if (self.duck_alive == 0 and self.active == 1):
            connection.send_channel(data['nick']+ " probiert eine nicht existente Ente zu befreunden.")
        if self.active == 0:
            connection.send_channel("Es läuft derzeit keine Entenjagd.")
    def shoot(self, data, connection):
        if self.duck_alive == 1:
            if randint(1,100) >97:
                connection.send_channel(data['nick'] + " trifft daneben.")
            else:
                self.duck_alive = 0
                self.addDeadDuck(data['nick'])
                connection.send_channel(self.build_duck_string(data['nick']))
            return
        if (self.duck_alive == 0 and self.active == 1):
            connection.send_channel(data['nick']+ " schießt ins Nichts.")
        if self.active == 0:
            connection.send_channel("Es läuft derzeit keine Entenjagd.")

    def update_on_ping(self, data, connection: Connection):
        if self.active == 0:
            return
        if 1 == randint(1,11):
            if self.duck_alive == 0:
                connection.send_channel("*. *. *. * <<w°)> *. *. * Quack!")
                self.duck_alive = 1

    def _is_idented_mod(self, data: dict, connection: Connection):
        return data['nick'] in self._config.mods and connection.is_idented(data['nick'])

    def getLiving(self, nick: str):
        duck_provider = DucksProvider()
        duck = duck_provider.get_ducks(nick)
        if duck is not None:
            return duck[1]
        else:
            return 0

    def getDead(self, nick: str):
        duck_provider = DucksProvider()
        duck = duck_provider.get_ducks(nick)
        if duck is not None:
            return duck[2]
        else:
            return 0

    def addDeadDuck(self, nick:str):
        self.writeDucks(nick, self.getLiving(nick), self.getDead(nick)+1)

    def addLivingDuck(self,nick:str):
        self.writeDucks(nick, self.getLiving(nick)+1, self.getDead(nick))

    def writeDucks(self, nick: str, living: int, dead: int):
        ducks_provider = DucksProvider()
        ducks_provider.save_or_replace(nick, living, dead)

    def build_duck_string(self, nick: str):
        return nick + " hat schon " +str(self.getLiving(nick))+ " befreundete "+self.pluralEnte(self.getLiving(nick))+" und " + str(self.getDead(nick)) + " getötete "+self.pluralEnte(self.getDead(nick))

    def pluralEnte(self, enten:int):
        if enten == 1:
            return "Ente"
        return "Enten"