import _thread

from FaustBot.Communication.Observable import Observable


class NoticeObservable(Observable):
    def notify_observers(self, data, connection):
        for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_notice, (observer, data, connection))

    def input(self, raw_data, connection):
        data = {'raw_data': raw_data, 'nick': raw_data.split('!')[0][1:], 'raw_nick': raw_data.split(' NOTICE ')[0][1:],
                'message': raw_data.split(':')[2]}
        self.notify_observers(data, connection)
