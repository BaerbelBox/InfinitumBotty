from FaustBot.Communication.Connection import Connection
from FaustBot.Model.i18n import i18n
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class GoogleObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.g') == -1:
            return
        i18n_server = i18n()
        lang = i18n_server.get_text('google_lang')
        t = i18n_server.get_text('google_tld')
        q = data['message'].split(' ')
        query = ''
        for word in q:
            if word.strip() != '.g':
                query += word + ' '
                #        g = google.search(query, tld=t, lang=lang, num=1, start=0, stop=0, pause=2.0)
                #        s = next(g)
                #        print(s)

                #        Connection.singleton().send_channel(g)
                #        if g has nonzero results:
                #            Connection.singleton().send_channel(data['nick'] + ', ' + i18n_server.get_text('google_fail'))
                #            return
        # Connection.singleton().send_channel(data['nick'] + ' ' + gefundenes erstes result)
        # Connection.singleton().send_channel(title von dem link)
        pass
