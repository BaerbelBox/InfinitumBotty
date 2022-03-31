import _thread

from FaustBot.Communication.Observable import Observable


class PingObservable(Observable):
    def input(self, raw_data, connection):
        data = {'raw': raw_data, 'server': ''}
        if raw_data.find('PING') == 0:
            data['server'] = raw_data.split('PING ')[1]
        else:
            return
        # hier kann noch gecheckt werden, ob data wirklich ein server ist, der ping haben will, oder sonstwas
        # finde heraus, wer zurückgepingt werden muss, und ob das überhaupt ein ping-request ist oder ein user sich
        # einen spass erlaubt hat
        self.notify_observers(data, connection)

    def notify_observers(self, data, connection):
        for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_ping, (observer, data, connection))
