
from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from random import randrange
from time import sleep
class MathRunObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return ['.s', '.startMath', '.stopMath']

    @staticmethod
    def help():
        return 'startMath startet eine Reihe von Aufgaben. StopMath beendet sie.'

    def __init__(self):
        super().__init__()
        self.players = {}
        self.solutionForGame = 0
        self.type = 0
        self.running = False
        self.oldSolution = 0

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.s ') != -1 :
            self.solution(data, connection)
        if data['message'].find('.startMath') != -1:
            self.start_math(data, connection)

    def solution(self, data, connection):
        nick = data["nick"]
        solutionByPlayer = data['message'].split()[1]
        if solutionByPlayer is None:
            connection.send_back("Sorry du hast keine Lösung angegeben " + nick, data)
            return
        if solutionByPlayer == str(self.solutionForGame):
            connection.send_channel("Korrekte Lösung " + nick)
            if nick not in self.players:
                self.players[nick] = 0
            self.players[nick] += 1
            self.oldSolution = self.solutionForGame
            self.start_math(data, connection)
            return
        if solutionByPlayer == str(self.oldSolution):
            connection.send_channel("Korrekte Lösung für das Problem davor " + nick)
            if nick not in self.players:
                self.players[nick] = 0
            self.players[nick] += 1
            return
        connection.send_channel("Sorry die Lösung ist falsch "+nick )

    def start_math(self, data, connection):
        summand1 = randrange(1,100)
        summand2 = randrange(1,11)
        operation = randrange(1,3)
        if operation == 1:
            self.solutionForGame = summand1 - summand2
            connection.send_channel(str(summand1) +" - "+str(summand2) +" = ?")
        if operation == 2:
            self.solutionForGame = summand1 + summand2
            connection.send_channel(str(summand1) +" + "+str(summand2) +" = ?")
        if not self.running:
            self.running = True
            self.stop_Timer(data, connection)

    def stop_math(self, data, connection):
        for player in self.players.keys():
            connection.send_channel(player + " hat\t" + str(self.players[player]) + "\t Punkte")
        connection.send_channel("Spiel beendet")
        self.players = {}
        self.solutionForGame = 0
        self.type = 0
        self.running = False

    def stop_Timer(self, data, connection):
        sleep(120)
        self.stop_math(data, connection)