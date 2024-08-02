import random

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from getraenkeOnlyGoodOnes import getraenkegoodones
from getraenke import getraenke
from essen import essen
from icecreamlist import icecream
from extras import giveextras
from snacks import snacks
from kekse import kekseGoodOnes


def _servier(receiver, item, requester):
    return f"\001ACTION serviert {receiver} {item}. Schöne Grüße von {requester}\001"


def _schenk(receiver, item, requester):
    return f"\001ACTION schenkt {receiver} {item} ein. Schöne Grüße von {requester}\001"


non_good_serveables = getraenke + essen + icecream + giveextras + snacks


class GiveDrinkToObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".give"]

    @staticmethod
    def help():
        return ".give NUTZER - serviert jemand anderem Getränke oder Snacks"

    def update_on_priv_msg(self, data, connection: Connection):
        if not data["message"].startswith(".give"):
            return
        receiver = type = None
        message_parts = data["messageCaseSensitive"].split()
        if len(message_parts) >= 2:
            receiver = message_parts[1]
        if len(message_parts) >= 3:
            type = message_parts[2].lower()
        if receiver is None:
            return
        requester = data["nick"].lower()
        if receiver.lower() == requester:
            if type == "kaffee":
                connection.send_back("Fehler 418: Ich bin eine Teekanne",data)
            else:
                connection.send_back("Bitte nutze .drink um dir selbst ein Getränk zu besorgen",data)
            return
        if type is None:
            connection.send_back(_schenk(receiver,random.choice(getraenkegoodones),requester),data)
            return
        if type in ["drink", "food", "cookie", "snack", "massage", "ice"]:
            if type == "drink":
                connection.send_back(_schenk(receiver,random.choice(getraenke),requester),data)
            elif type == "food":
                connection.send_back(_servier(receiver,random.choice(essen),requester),data)
            elif type == "cookie":
                connection.send_back(_servier(receiver,random.choice(kekseGoodOnes),requester),data)
            elif type == "snack":
                connection.send_back(_servier(receiver,random.choice(snacks),requester),data)
            elif type == "ice":
                connection.send_back(_servier(receiver,random.choice(icecream),requester),data)
            elif type == "massage":
                connection.send_back(
                    f"\001ACTION knetet {receiver} feste den Rücken durch. {requester} meinte ich solle dir was Gutes tun.\001",
                    data,
                )
            return
        matchingGoodDrinks = [drink for drink in getraenkegoodones if type in drink.lower()]
        if matchingGoodDrinks:
            connection.send_back(_schenk(receiver,random.choice(matchingGoodDrinks),requester),data)
            return

        matchingServeables = [serveable for serveable in non_good_serveables if type in serveable.lower()]
        if matchingServeables:
            connection.send_back(_servier(receiver,random.choice(matchingServeables),requester),data)
            return

        connection.send_back(
            f"Tut mir leid {requester}, {type} haben wir nicht auf der Karte!", data
        )
