from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

import random

class LetterObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".abc"]

    @staticmethod
    def help():
        return ".abc - wählt einen zufälligen Buchstaben aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.abc') == -1:
            return

        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z', 'ä', 'ö', 'ü']

        #choose a random letter from alphabet list
        letter = random.choice(alphabet).upper()

        connection.send_back('Gewählter Buchstabe: ' + letter, data)