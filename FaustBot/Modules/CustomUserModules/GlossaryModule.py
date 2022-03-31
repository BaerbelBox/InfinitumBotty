from FaustBot.Communication.Connection import Connection
from FaustBot.Model.Config import Config
from FaustBot.Model.GlossaryProvider import GlossaryProvider
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from FaustBot.Modules.WikiObserver import WikiObserver

class GlossaryModule(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [GlossaryModule._ADD_EXPLANATION,
                GlossaryModule._REMOVE_EXPLANATION,
                GlossaryModule._QUERY_EXPLANATION]

    @staticmethod
    def help():
        return None

    _QUERY_EXPLANATION = '.?'
    _REMOVE_EXPLANATION = '.?-'
    _ADD_EXPLANATION = '.?+'

    def __init__(self, config: Config):
        super().__init__()
        self._config = config

    def update_on_priv_msg(self, data, connection: Connection):
        msg = data['message']
        if not -1 == msg.find(GlossaryModule._REMOVE_EXPLANATION):
            self._remove_query(data, connection)
        elif not -1 == msg.find(GlossaryModule._ADD_EXPLANATION):
            self._add_query(data, connection)
        elif not -1 == msg.find(GlossaryModule._QUERY_EXPLANATION):
            self._answer_query(data, connection)

    def _answer_query(self, data, connection: Connection):
        """
        :param data: 
        :param connection: 
        :return: 
        """
        glossary_provider = GlossaryProvider()
        split = data['message'].split(GlossaryModule._QUERY_EXPLANATION)
        if not len(split) == 2:
            return
        answer = glossary_provider.get_explanation(split[1].strip())
        if answer is None or answer[1] is None or answer[1].strip() == '':
            if split[1].strip() == '':
                return
#            connection.send_back("Tut mir leid, " + data['nick'] + ". Für " + split[1].strip() +
#                                 " habe ich noch keinen Eintrag. Aber Wikipedia sagt dazu:", data)
            wikiObserver = WikiObserver()
            wikiObserver.config = self.config
            data2 = data.copy()
            data2['message'] = '.w '+split[1]+" \r\n"
            wikiObserver.update_on_priv_msg(data2, connection)
        else:
            connection.send_back(data['nick'] + ": " + split[1] + " - " + answer[1], data)

    def _remove_query(self, data, connection: Connection):
        """

        :param data: 
        :param connection: 
        :return: 
        """
        if not self._is_idented_mod(data, connection):
            connection.send_back("Dir fehlen die Berechtigungen zum Löschen von Einträgen, " + data['nick'] + ".", data)
            return
        glossary_provider = GlossaryProvider()
        split = data['message'].split(GlossaryModule._REMOVE_EXPLANATION)
        if not len(split) == 2:
            return
        glossary_provider.delete_explanation(split[1])
        connection.send_back("Der Eintrag zu " + split[1] + " wurde gelöscht, " + data['nick'] + ".", data)

    def _add_query(self, data, connection: Connection):
        """
        
        :param data: 
        :param connection: 
        :return: 
        """
        if not self._is_idented_mod(data, connection):
            connection.send_back("Dir fehlen leider die Rechte zum Hinzufügen von Einträgen, " + data['nick'] + ".",
                                 data)
            return
        msg = data['message'].split(GlossaryModule._ADD_EXPLANATION)[1].strip()
        split = msg.split(' ', 1)
        glossary_provider = GlossaryProvider()
        glossary_provider.save_or_replace(split[0], split[1])
        connection.send_back(data['nick'] + ": der Eintrag zu " + split[0] + " wurde gespeichert.", data)

    def _is_idented_mod(self, data: dict, connection: Connection):
        return data['nick'] in self._config.mods and connection.is_idented(data['nick'])
