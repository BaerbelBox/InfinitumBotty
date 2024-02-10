from time import sleep
from wikipedia import wikipedia
from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class JokeObserver(PrivMsgObserverPrototype):
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
        listener = [".basteln", ".craft"]

        return listener

    @staticmethod
    def help():
        return ".basteln - Botty bastelt etwas"

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
        connection.send_back("\001ACTION rennt in die Werkstatt!\001", data)
        sleep(5)
        connection.send_back("\001ACTION poltert herum!", data)

        # Determine, what Botty has built (random wikipedia article)
        spiegelei = wikipedia.random(1)
        sleep(5)
        connection.send_back(
                f"\001ACTION kommt zurück und hat {spiegelei} gebastelt.\001", data)
