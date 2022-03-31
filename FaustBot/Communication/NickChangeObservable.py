import _thread

from FaustBot.Communication.Observable import Observable


class NickChangeObservable(Observable):
    def input(self, raw_data, connection):
        data = {'raw': raw_data, 'old_nick': raw_data.split('!')[0][1:],
                'new_nick': raw_data.split('NICK ')[1].split(':')[1], 'raw_nick': raw_data.split(' NICK')[0][1:]}
        self.notify_observers(data, connection)

    def notify_observers(self, data, connection):
        for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_nick_change, (observer, data, connection))
