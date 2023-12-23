
from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from collections import defaultdict
from time import sleep


class WordRunObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return ['.a', '.add', '.begin', '.end', '.wordrun']

    @staticmethod
    def help():
        return 'Wordrun Spiel. Starten mit .begin <Silbe> oder .end <Silbe>. Antwort hinzufügen mit .a <Antwort> oder .add <Antwort> Mehr Details mit .wordrun im Query abfragen.'

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
          if data['message'].startswith('.a ') or data['message'].startswith('.add '):
            self.add(data, connection)
          if data['message'].startswith('.begin '):
                self.begin_word(data, connection)
          if data['message'].startswith('.end '):
                self.end_word(data, connection)
          if data['message'].startswith('.wordrun'):
                self.rules(data, connection)
   
    def add(self, data, connection):
        if self.gamestatus == 0:
            connection.send_channel("Es läuft derzeit kein Wordrun, bitte einen neuen mit .begin <Silbe> oder .end <Silbe> erstellen!")
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
            if word == '.a' or word == '.add':
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
            s = s + p + ": "+str(player_score[p])+ "; "
        connection.send_channel(s)
        self.gamestatus = 0
        self.player = {}

    def rules(self, data, connection):
        if data['channel'] == connection.details.get_channel():
            connection.send_back("Spielregeln bitte im Query (Privatchat) mit dem Bot abfragen", data)
            return
        connection.send_back('Wordrun Spiel: So viele Wörter wie möglich finden, die mit der vorgegebenen Silbe anfangen oder aufhören.', data)
        connection.send_back('Spiel starten mit .begin <Silbe>, um ein Spiel zu starten, bei dem die Antworten mit <Silbe> anfangen müssen.', data)
        connection.send_back('Spiel starten mit .end <Silbe>, um ein Spiel zu starten, bei dem die Antworten mit <Silbe> enden müssen.', data)
        connection.send_back('Antwort hinzufügen mit .a <Antwort> oder .add <Antwort>', data)
        connection.send_back('Es können auch mehrere Antworten in einer Zeile angegeben werden', data)
        connection.send_back('Das Spiel dauert 3 Minuten. Für jede gültige Antwort gibt es 1 Punkt.', data)

