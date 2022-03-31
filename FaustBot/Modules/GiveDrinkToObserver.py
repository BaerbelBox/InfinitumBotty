import random

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from getraenkeOnlyGoodOnes import getraenkegoodones
from getraenke import getraenke
from essen import essen
from icecreamlist import icecream
from extras import giveextras
from snacks import snacks
kekse = ['einen Schokoladenkeks', 'einen Vanillekeks', 'einen Doppelkeks',
         'einen Keks', 'einen Erdbeerkeks', 'einen Schokoladen-Cheesecake-Keks',
         'einen Glückskeks', 'einen Scherzkeks', 'einen Unglückskeks']

class GiveDrinkToObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".givedrink"]

    @staticmethod
    def help():
        return ".givedrink NUTZER - schenkt jemand anders ein Getränke aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.give') == -1:
            return
        receiver = data['message'].split()[1]
        if receiver == data['nick']:
            type = data['message'].split()[2]
            if type is not None:
                if type.lower() == "kaffee":
                    connection.send_back('Fehler 418 Ich bin eine Teekanne', data)
                    return
            connection.send_back('Bitte nutze .drink um dir selbst ein Getränk zu besorgen', data)
            return
        if len(data['message'].split()) < 3:
            connection.send_back(
                '\001ACTION serviert ' + receiver + ' ' + random.choice(getraenkegoodones) + '. Schöne Grüße von ' + data[
                    'nick'] + '\001', data)
            return
        type = data['message'].split()[2]
        if type is not None:
            matchingDrinks = []
            for drink in getraenkegoodones:
                if type.lower() in drink.lower():
                    matchingDrinks.append(drink)
            if matchingDrinks:
                connection.send_back(
                    '\001ACTION serviert ' + receiver + ' ' + random.choice(matchingDrinks) + '. Schöne Grüße von ' + data[
                        'nick'] + '\001', data)
                return
            if type.lower() == "drink":
                connection.send_back(
                    '\001ACTION serviert ' + receiver + ' ' + random.choice(getraenke) + '. Schöne Grüße von ' +
                    data[
                        'nick'] + '\001', data)
                return

            if type.lower() == "food":
                connection.send_back(
                    '\001ACTION serviert ' + receiver + ' ' + random.choice(essen) + '. Schöne Grüße von ' +
                    data[
                        'nick'] + '\001', data)
                return

            if type.lower() == "cookie":
                connection.send_back(
                    '\001ACTION serviert ' + receiver + ' ' + random.choice(kekse) + '. Schöne Grüße von ' +
                    data[
                        'nick'] + '\001', data)
                return
            if type.lower() == "snack":
                connection.send_back(
                    '\001ACTION serviert ' + receiver + ' ' + random.choice(snacks) + '. Schöne Grüße von ' +
                    data[
                        'nick'] + '\001', data)
                return
            if type.lower() == "massage":
                connection.send_back(
                    '\001ACTION knetet ' + receiver + ' feste den Rücken durch. ' +
                    data[
                        'nick'] + ' meinte ich solle dir was gutes tun. \001', data)
                return
            for drink in getraenke+essen+icecream+giveextras+snacks:
                if type.lower() in drink.lower():
                    matchingDrinks.append(drink)
            if matchingDrinks:
                connection.send_back(
                    '\001ACTION serviert ' + receiver + ' ' + random.choice(matchingDrinks) + '. Schöne Grüße von ' +
                    data[
                        'nick'] + '\001', data)
                return
            else:
                connection.send_back(
                    'Tut mir leid ' + data['nick'] + ', '+ type+' haben wir nicht auf der Karte!', data)
                return
        connection.send_back('\001ACTION serviert ' + receiver + ' ' + random.choice(getraenkegoodones) + '. Schöne Grüße von '+data['nick']+'\001', data)

