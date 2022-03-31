
from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from collections import defaultdict
from time import sleep


class WordRunObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return ['.a', '.add', '.begin', '.end']

    @staticmethod
    def help():
        return 'hangman game'

    def __init__(self):
        super().__init__()
        self.player = {}
        self.gamestatus = 0
        """
        0 = Kein Spiel
        1 = Spiel mit Silbe am Anfang
        2 = Spiel mit Silbe am Ende
        """
        self.syllable = ""

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.a ') != -1 or data['message'].find('.add ') != -1:
            self.add(data, connection)
        if data['message'].find('.begin ') != -1:
            self.begin_word(data, connection)
        if data['message'].find('.end ') != -1:
            self.end_word(data, connection)

    def add(self, data, connection):
        if self.gamestatus == 0:
            connection.send_channel("Es läuft derzeit kein Wordrun, bitte einen neuen mit .begin <Silbe> oder .end <silbe> erstellen!")
            return
        if self.gamestatus == 1 or self.gamestatus == 2:
            self.check_word(data["nick"], data['message'], connection)

    def begin_word(self, data, connection):
        if self.gamestatus != 0:
            connection.send_channel("Es läuft bereits ein Spiel")
            return
        self.gamestatus = 1
        self.handle_game(data,connection)

    def end_word(self, data, connection):
        if self.gamestatus != 0:
            connection.send_channel("Es läuft bereits ein Spiel")
            return
        self.gamestatus = 2
        self.handle_game(data,connection)

    def check_word(self,player , message, connection):
        for word in message.split():
            if word == '.a':
                continue
            if self.gamestatus == 1:
                if word.upper().startswith(self.syllable.upper()):
                    self.add_to_dict(player, word, connection)
            if self.gamestatus == 2:
                if word.upper().endswith(self.syllable.upper()):
                    self.add_to_dict(player, word, connection)

    def add_to_dict(self, nick, word, connection):
        for p in self.player.keys():
            for w in self.player[p]:
                if w.upper() == word.upper():
                    connection.send_channel("Das Wort "+word+" wurde bereits von "+p+ " genannt")
                    return
        if nick not in self.player:
            self.player[nick] = []
        self.player[nick].append(word)

    def handle_game(self, data, connection):
        self.syllable = data["message"].split()[1]
        if self.gamestatus == 1:
            connection.send_channel("Das Wort muss mit " + self.syllable + "- beginnen")
        if self.gamestatus == 2:
            connection.send_channel("Das Wort muss mit -" + self.syllable + " enden")
        sleep(150)
        connection.send_channel("Noch 30 Sekunden")
        sleep(30)
        player_score = defaultdict(int)
        s = "Folgende Ergebnisse: "
        for p in self.player.keys():
            for w in self.player[p]:
                print(p+" "+w)
                player_score[p] += 1
        for p in self.player.keys():
            s = s + p + " : "+str(player_score[p])+ "; "
        connection.send_channel(s)
        self.gamestatus = 0
        self.player = {}