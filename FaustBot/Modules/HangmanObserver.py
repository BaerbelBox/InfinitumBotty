
from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from FaustBot.Model.ScoreProvider import ScoreProvider
from FaustBot.Model.HanDatabaseProvider import HanDatabaseProvider
from collections import defaultdict
from threading import Lock
import csv
import random
import time
import datetime

class HangmanObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return ['.guess', '.word', '.stop', '.hint', '.score', '.spielregeln']

    @staticmethod
    def help():
        return 'hangman game'

    def __init__(self):
        super().__init__()
        HangmanObserver.lock = Lock()
        self.word = ''
        self.guesses = ['-', '/', ' ', '_','.']
        self.tries_left = 0
        self.wrong_guessed = []
        self.worder = ''
        self.wrongly_guessedWords = []
        self.time = time.time()

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.guess ') != -1:
            self.guess(data, connection)
            return
        if data['message'].find('.word ') != -1:
            self.take_word(data, connection)
        if data['message'].find('.han') != -1 and not data['message'].find('.handelete')!= -1 and not data['message'].find('hanadd'
        ) != -1:
            self.start_solo_game(data, connection)
        if data['message'].find('hanadd') != -1:
            self.han_user_add(data, connection)
        if data['message'].find('.stop') != -1 and not data['message'].find('.stophunt') != -1 \
                and not data['message'].find('.stopMath') != -1:
            connection.send_channel("Spiel gestoppt. Das Wort war: " + self.word + " in: "+self.timeRelapsedString())
            self.word = ''
            self.guesses = []
            self.tries_left = 0
            self.wrong_guessed = []
            self.worder = ''
            self.wrongly_guessedWords = []
            self.worder = ''
        if data['message'].find('.hint') != -1:
            self.hint(data, connection)
        if data['message'].find('.score') != -1:
            self.print_score(data, connection)
        if data['message'].find('.spielregeln') != -1:
            self.rules(data, connection)
        if data['message'].find('.look') != -1:
            self.look(data, connection)
        if data['message'].find('.resetscore') != -1:
            self.reset(data,connection)
        if data['message'].find('.handelete') != -1:
            self.delete_HanWord(data, connection)

    def delete_HanWord(self,data,connection):
        if not self._is_idented_mod(data, connection):
            connection.send_back(
                "Du hast keine Berechtigung Wörter zu löschen " + data['nick'], data)
            return
        if data['message'].split(' ')[1] is not None:
            self.deleteHanWord(data['message'].split(' ')[1].upper())
            connection.send_back("Das Wort "+data['message'].split(' ')[1].upper()+" wurde gelöscht, " + data['nick'], data)

    def reset(self,data,connection):
        score_provider = ScoreProvider()
        score_provider.delete_score(data['nick'])
        connection.send_back("Dein Score wurde gelöscht "+data['nick'], data)

    def look(self,data, connection):
        if self.worder != '':
            connection.send_channel("Das Wort kommt von: "+self.worder )
        connection.send_channel(self.prepare_word(data))
        self.hint(data,connection)

    def print_score(self, data, connection):
        punkte = self.getScore(data['nick'])
        connection.send_back(data['nick']+" hat einen Hangman-Score von: " + str(punkte), data)

    def hint(self, data, connection):
        wrongGuessesString = ""
        if len(self.wrong_guessed) == 0 and len(self.wrongly_guessedWords) == 0:
            wrongGuessesString = "Noch keine falschen Buchstaben."
        if len(self.wrong_guessed) > 0:
            wrongGuessesString += "Falsch geratene Buchstaben bis jetzt: "
            for w in self.wrong_guessed:
                if w == self.wrong_guessed[0]:
                    wrongGuessesString += w
                else:
                    wrongGuessesString += ", " + w
        
        # Append wrongly guessed words    
        for w in self.wrongly_guessedWords:
            if w == self.wrongly_guessedWords[0]:
                if len(self.wrong_guessed) > 0:
                    wrongGuessesString += " | "
                wrongGuessesString += "Falsche Wörter: " + w
            else:
                wrongGuessesString += ", " + w
        if self.worder == "":
            wrongGuessesString = ""
        else:
            connection.send_back(wrongGuessesString, data)

    def start_solo_game(self, data, connection):
        if self.word == '':
            self.time = time.time()
            self.word = self.getRandomHanWord()
            self.guesses = ['-', '/', ' ', '_','.']
            self.wrong_guessed = []
            self.tries_left = 11
            self.wrongly_guessedWords = []
            connection.send_channel("Automatisch gewähltes Wort")
            self.worder = "Botty"
            connection.send_channel(self.prepare_word(data))
        else:
            connection.send_back("Sorry es läuft bereits ein Wort", data)

    def guess(self, data, connection):
        if data['channel'] != connection.details.get_channel():
            connection.send_back("Sorry kein raten im Query", data)
            return
        guess = data['message'].split(' ')[1].upper()
        if self.tries_left < 1:
            connection.send_channel("Flüstere mir ein neues Wort mit .word WORT")
            return
        word_unique_chars = len(set(self.word))
        if guess == self.word:
            score = word_unique_chars * self.count_missing_unique()
            self.addToScore(data['nick'], int(score))
            self.word = ''
            self.worder = ''
            connection.send_channel("Das ist korrekt: " + guess + " gelöst hat: "+data["nick"]+ " in: "+self.timeRelapsedString())
            self.giveExtraPointsInTime(data["nick"])
            return
        if guess in self.word:
            if guess not in self.guesses:
                score = word_unique_chars / 2
                self.addToScore(data['nick'], int(score))
                self.guesses.append(guess)
        else:
            self.tries_left -= 1
            punishment_factor = 1
            if guess in self.guesses:
                punishment_factor = 2
            self.addToScore(data['nick'], -1)
            #(int((word_unique_chars / 20) * punishment_factor * 10))

            # append thread safe wrongly guessed characters and words
            HangmanObserver.lock.acquire()
            try:
                if guess not in self.wrong_guessed:
                    if len(guess) == 1:
                        self.wrong_guessed.append(guess)
                    else:
                        self.wrongly_guessedWords.append(guess)
            finally:
                HangmanObserver.lock.release()

        connection.send_channel(self.prepare_word(data))

    def take_word(self, data, connection):
        if self.word == '':
            self.time =time.time()
            if data['message'].split(' ')[1] is not None:
                self.addHanWord(data['message'].split(' ')[1].upper())
            log = open('HangmanLog', 'a')
            log.write(data['nick'] + ' ; ' + data['message'].split(' ')[1].upper() + '\n')
            log.close()
            self.word = data['message'].split(' ')[1].upper()
            self.guesses = ['-', '/', ' ', '_','.']
            self.wrong_guessed = []
            self.tries_left = 11
            self.wrongly_guessedWords = []
            connection.send_back("Danke für das Wort, es ist nun im Spiel!", data)
            connection.send_channel("Das Wort ist von: "+data['nick'])
            self.worder = data['nick']
            connection.send_channel(self.prepare_word(data))
        else:
            connection.send_back("Sorry es läuft bereits ein Wort", data)
    def han_user_add(self, data, connection):
        if data['message'].split(' ')[1] is not None:
            self.addHanWord(data['message'].split(' ')[1].upper())
            connection.send_channel("Das Wort "+data['message'].split(' ')[1].upper() +" wurde von "+ data['nick']+ " hinzugefügt")
    def prepare_word(self, data):
        outWord = ""
        failedChars = 0
        for char in self.word:
            if char in self.guesses:
                outWord += char + " "
            else:
                outWord += "_ "
                failedChars += 1
        if failedChars == 0:
            if len(self.word) > 0:
                outWord = "Das ist korrekt: " + self.word + " gelöst hat: "+data["nick"]+ " in : "+self.timeRelapsedString()
                self.giveExtraPointsInTime(data["nick"])
                self.addToScore(data['nick'], 5)
                self.word = ''
                self.worder = ''
                return outWord
            else:
                outWord = "Bitte gib ein neues Wort mit .word im Query an."
                return outWord
        if self.tries_left == 0:
            self.addToScore(self.worder,11)
            outWord = "Das richtige Wort wäre gewesen: " + self.word + " in: "+self.timeRelapsedString()
            self.word = ''
            self.worder = ''
            return outWord
        outWord += "Verbleibende Rateversuche: "+str(self.tries_left)
        return outWord

    def count_missing(self):
        missing_chars = 0
        for char in self.word:
            if char not in self.guesses:
                missing_chars += 1
        return missing_chars

    def count_missing_unique(self):
        return len(set(self.word) - set(self.guesses))

    def rules(self, data, connection):
        if data['channel'] == connection.details.get_channel():
            connection.send_back("Spielregeln bitte im Query abfragen",data)
            return
        connection.send_back("""Wort starten mit ".word Wort" im Query mit dem Bot""", data)
        connection.send_back("""Raten mit ".guess Buchstabe" im Channel""", data)
        connection.send_back("""Geraten werden können einzelne Buchstaben oder das ganze Wort.""", data)
        connection.send_back("""Alle dürfen durcheinander raten. Es gibt keine Reihenfolge.""", data)
        connection.send_back("""".hint" gibt alle bereits falsch geratenen Buchstaben aus.""", data)
        connection.send_back("""Bei 2 verbleibenden Versuchen darf nach einem Tipp vom Steller des Wortes gefragt 
        werden.""", data)
        connection.send_back("""Wer ein Wort errät, darf das nächste stellen.""", data)
        connection.send_back("""Wird ein Wort nicht gelöst, darf derjenige, der es gestellt hat, nochmal.""", data)
        connection.send_back("""Zulässig sind alle Wörter, die deutsch oder im deutschen Sprachraum geläufig sind.""", data)

    def getScore(self, nick:str):
        score_provider = ScoreProvider()
        score = score_provider.get_score(nick)
        if score is not None:
            return score[1]        
        else:
            return 0
    
    def writeScore(self, nick:str, score:int):
        score_provider = ScoreProvider()
        score_provider.save_or_replace(nick, score)
    
    def addToScore(self, nick:str, add_score: int):
        score = self.getScore(nick)
        self.writeScore(nick, score + add_score)

    def addHanWord(self, hanWord:str):
        hanDB = HanDatabaseProvider()
        hanDB.addWord(hanWord.strip().upper())

    def getRandomHanWord(self):
        hanDB = HanDatabaseProvider()
        word = hanDB.get_random_word()
        if word is not None:
            return word[0].upper()
        else:
            return "dummywort".upper()

    def deleteHanWord(self, hanWord:str):
        hanDB = HanDatabaseProvider()
        hanDB.delete_hanWord(hanWord.strip().upper())

    def _is_idented_mod(self, data: dict, connection: Connection):
        return data['nick'] in self._config.mods and connection.is_idented(data['nick'])

    def timeRelapsedString(self):
        delta = time.time()-self.time
        return str(datetime.timedelta(seconds= delta))

    def giveExtraPointsInTime(self, nick):
        delta = time.time()-self.time
        if delta <30:
            self.addToScore(nick, 5)
        if delta <60:
            self.addToScore(nick, 5)