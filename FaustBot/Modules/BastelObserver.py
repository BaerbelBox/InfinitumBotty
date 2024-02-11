from time import sleep
from wikipedia import wikipedia
from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class BastelObserver(PrivMsgObserverPrototype):
    def __init__(self):
        super().__init__()
        self.annoyed: int = 0

    @staticmethod
    def cmd():
        """
        @name cmd
        @brief Register the commands to act on

        Args:
            @param
        Returns:
            listener Python list with strings to listen for.
        """
        listener = [".craft"]

        return listener

    @staticmethod
    def help():
        return ".craft - Botty bastelt etwas"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        """
        @name update_on_priv_msg
        @brief Handle botty's crafting process

        Args:
            @param self@param data: dict@param connection: Connection
        Returns:

        """
        if data['message'].find('.craft') == -1:
            return

        # Start not more than one process with a longer iteration (15 seconds)
        if self.annoyed > 0:
            if self.annoyed == 1:
                connection.send_back("Lass mich in Ruhe arbeiten!", data)
            elif self.annoyed == 2:
                connection.send_back("Ich muss mich konzentrieren!", data)
            elif self.annoyed == 3:
                connection.send_back("So kann ich nicht arbeiten!", data)
            else:
                connection.send_back("\001ACTION wirft mit Werkzeug um sich!\001", data)

            # Bot is getting more annoyed when hit on multiple times
            # self.annoyed is again checked against zero, as it's more likely to prevent a deadlock
            if self.annoyed > 0:
                self.annoyed = self.annoyed + 1
        else:
            self.annoyed = 1
            connection.send_back("\001ACTION rennt in die Werkstatt.\001", data)
            sleep(10)
            connection.send_back("\001ACTION poltert herum.", data)

            # Determine, what Botty has built (random wikipedia article)
            wikipedia.set_lang('de')
            crafted_object = wikipedia.random(1)
            sleep(5)
            connection.send_back(
                    f"\001ACTION kommt zurück und hat {crafted_object} gebastelt.\001", data)
            self.annoyed = 0
