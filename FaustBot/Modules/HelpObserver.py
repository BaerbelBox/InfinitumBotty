from types import NoneType
from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class HelpObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".help"]

    @staticmethod
    def help():
        return ".help <Befehl> - zeigt Hilftexte zu <Befehl> an. Für eine Liste aller verfügbaren Befehle: .help all"

    def update_on_priv_msg(self, data, connection: Connection):
        msg = data["message"]
        command = ""
        if not msg.startswith(".help"):
            return
        if len(msg.split(' ')) > 1:
            command = msg.split(' ')[1]
            if command == 'all':
                self.show_available_commands(data, connection)
            else:    
                if not command.startswith("."):
                    command = '.' + command
                self.show_help_for_command(command, data, connection)
        else:
            connection.send_back(self.help(), data)

    def collect_commands(self, connection):
        all_cmd = []
        for observer in connection.priv_msg_observable.get_observer():
            cmds = observer.cmd()
            if cmds is not None:
                all_cmd.extend(cmds)
        print(all_cmd)
        return all_cmd

    def show_available_commands(self, data, connection):
        if data["channel"] == connection.details.get_channel():
            all_cmd = []
            all_cmd = self.collect_commands(connection)
            msg = ", ".join(all_cmd)
            msg = "Bekannte Befehle: " + msg
            connection.send_back(msg, data)
        else:
            all_help = [m.help() for m in connection.priv_msg_observable.get_observer()]
            for help_msg in all_help:
                if help_msg is not None:
                    connection.send_back(help_msg, data)

    def show_help_for_command(self, command, data, connection):
        for observer in connection.priv_msg_observable.get_observer():
            if observer.cmd() is not None:
                if command in observer.cmd():
                    print(observer.help())
                    connection.send_back(observer.help(), data)
        

       
