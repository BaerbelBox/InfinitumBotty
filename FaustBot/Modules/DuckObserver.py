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
        self.streak = 0
        self.streakname = ""

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
                self.duckAchievments(data['nick'], connection)
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
                self.duckAchievments(data['nick'], connection)
            return
        if (self.duck_alive == 0 and self.active == 1):
            connection.send_channel(data['nick']+ " schießt ins Nichts.")
        if self.active == 0:
            connection.send_channel("Es läuft derzeit keine Entenjagd.")

    def update_on_ping(self, data, connection: Connection):
        if self.active == 0:
            return
        if 1 == randint(1,15):
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
        duckstring = ""
        livingDucks = self.getLiving(nick)
        deadDucks = self.getDead(nick)
        if livingDucks > 1:
            duckstring = duckstring + nick + " hat schon " +str(livingDucks)+ " befreundete Enten und "
        elif livingDucks == 1:
            duckstring = duckstring + nick + " hat schon eine befreundete Ente und "
        elif livingDucks == 0:
            duckstring = duckstring + nick + " hat noch keine befreundeten Enten und "
        if deadDucks > 1:
            duckstring = duckstring + str(deadDucks) + " getötete Enten"
        elif deadDucks == 1:
            duckstring = duckstring +"eine getötete Ente"
        elif deadDucks == 0:
            duckstring = duckstring+"keine getöteten Enten"
        return duckstring

    def duckAchievments(self, nick, connection):
        dead = self.getDead(nick)
        living  = self.getLiving(nick)
        if dead == 0:
            if living == 5:
                connection.send_channel(nick + " hat den Titel 'kleiner Entenfreund' erreicht")
            elif living == 66:
                connection.send_channel(nick + " hat den Titel 'Entenfreund' erreicht")
            elif living == 111:
                connection.send_channel(nick + " hat den Titel 'großer Entenfreund' erreicht")
            elif living == 555:
                connection.send_channel(nick + " hat den Titel 'Kleiner Entenmonarch' erreicht")
            elif living == 1111:
                connection.send_channel(nick + " hat den Titel 'Entenmonarch' erreicht")
            elif living == 2222:
                connection.send_channel(nick + " hat den Titel 'großer Entenmonarch' erreicht")
            elif living == 3333:
                connection.send_channel(nick + " hat den Titel 'Enten veehren dich als ihre Gottheit!' erreicht")

        if living == 0:
            if dead == 5:
                connection.send_channel(nick + " hat den Titel 'kleiner Entenmörder' erreicht")
            elif dead == 66:
                connection.send_channel(nick + " hat den Titel 'Entenmörder' erreicht")
            elif dead == 111:
                connection.send_channel(nick + " hat den Titel 'großer Entenmörder' erreicht")
            elif dead == 555:
                connection.send_channel(nick + " hat den Titel 'kleiner Entenmassenmörder' erreicht")
            elif dead == 1111:
                connection.send_channel(nick + " hat den Titel 'Entenmassenmörder' erreicht")
            elif dead == 2222:
                connection.send_channel(nick + " hat den Titel 'großer Entenmassenmörder' erreicht")
            elif dead == 3333:
                connection.send_channel(nick + " hat den Titel 'du musst Enten wirklich hassen' erreicht")
        if dead > 0 and living > 0:
            if living + dead == 5:
                connection.send_channel(nick + " hat den Titel 'Enten könnten Angst vor dir haben' erreicht")
            elif living+ dead == 66:
                connection.send_channel(nick + " hat den Titel 'Enten, Enten. So viele Enten' erreicht")
            elif living + dead == 111:
                connection.send_channel(nick + " hat den Titel 'Ich liebe Enten' erreicht")
            elif living + dead == 555:
                connection.send_channel(nick + " hat den Titel 'Auf dem Grill und als Freund. Enten sind mein Leben' erreicht")
            elif living + dead == 1111:
                connection.send_channel(nick + " hat den Titel 'Durchgespielt' erreicht")
            elif living + dead == 2222:
                connection.send_channel(nick + " hat den Titel 'Immernoch im Spiel' erreicht")
            elif living + dead == 3333:
                connection.send_channel(nick + " hat den Titel 'Alter!' erreicht")

        if nick == self.streakname:
            self.streak+=1
        else:
            self.streak = 1
            self.streakname = nick

        if self.streak == 3:
            connection.send_channel(nick + " hat einen Lauf")
        elif self.streak == 5:
            connection.send_channel(nick + " ist nicht aufhaltbar")
        elif self.streak == 15:
            connection.send_channel(nick + " spielt wohl allein")
