from FaustBot.Communication import Connection
from FaustBot.Model.Introduction import IntroductionProvider
from FaustBot.Modules import UserList
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class IntroductionObserver(PrivMsgObserverPrototype):
    def __init__(self, user_list: UserList):
        super().__init__()
        self.userList = user_list

    @staticmethod
    def cmd():
        return [".me"]

    @staticmethod
    def help():
        return ".me - kann von registrierten Nutzern verwendet werden um eine Vorstellung zu speichern"

    def update_on_priv_msg(self, data, connection: Connection):
        msg = data["message"]
        nick = data["nick"]
        if not msg.startswith(".me") and not msg.startswith(".me-"):
            return
        if not self.authenticated(nick, connection):
            connection.send_back("Für die Nutzung von .me ist es zwingend erforderlich, einen registrierten Nick zu "
                                 "haben sowie eingeloggt zu sein. Wie dies geht, erfährst du unter "
                                 "https://freenode.net/kb/answer/registration", data)
            return
        intro_provider = IntroductionProvider()
        msg = msg.split('.me')[1].strip()
        if len(msg) == 0:
            intro = intro_provider.get_intro(nick)
            text = ""
            if intro is not None:
                text = nick + " ist " + intro[1]
            else:
                text = nick + " für dich gibt es noch keinen Eintrag, vielleicht magst du ja mittels .me <intro> noch " \
                              "einen hinzufügen? "
            connection.send_back(text, data)
        elif len(msg) == 1 and '-' in msg:
            intro_provider.delete_intro(nick)
            connection.send_back(nick + " dein Intro wurde gelöscht!", data)
        else:
            intro = msg.strip()
            intro_provider.save_or_replace(nick, intro)
            connection.send_back(
                nick + ": Dein Intro wurde gespeichert! Mittels .me- kannst du deinen Eintrag wieder löschen.", data)
            text = nick + " ist " + intro_provider.get_intro(nick)[1]
            connection.send_back(text, data)

    def authenticated(self, nick: str, connection: Connection):
        return nick in self.userList.userList and \
               connection.is_idented(nick)
