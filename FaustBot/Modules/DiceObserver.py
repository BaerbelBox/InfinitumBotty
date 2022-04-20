from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

import random

class DiceObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".zahl"]

    @staticmethod
    def help():
        return ".zahl n - Wirft einen n-seitigen Würfel"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.zahl') == -1:
            return

        #roll a die with given number of sides, standard is 6
        dice_sides = 6
        
        if len(data['message'].split(' ')) > 1:
            found_at_index = data['message'].split(' ').index('.zahl')
            if data['message'].split(' ')[-1] == '.zahl':
                dice_sides = 6
            else:
                dice_sides = (data['message'].split(' ')[found_at_index + 1])
                if dice_sides.isdigit():
                    dice_sides = int(dice_sides)
                else:
                    dice_sides = 6
        result = random.randint(1, dice_sides)

        connection.send_back(data['nick'] + ' wirft einen ' + str(dice_sides) + '-seitigen Würfel und bekommt ' + str(result), data)