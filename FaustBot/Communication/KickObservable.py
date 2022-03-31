import _thread

from FaustBot.Communication.Observable import Observable


class KickObservable(Observable):
    def input(self, raw_data, connection):
        data = {}
        print(raw_data)
        data['raw'] = raw_data
        data['op'] = raw_data.split('!')[0][1:]
        data['channel'] = raw_data.split('KICK ')[1].split(' :')[0].split(' ')[0]
        data['nick'] = raw_data.split('KICK ')[1].split(' :')[0].split(' ')[1]
        data['raw_op'] = raw_data.split(' KICK')[0][1:]
        data['reason'] = raw_data.split('KICK ')[1].split(' :')[1]
        self.notify_observers(data, connection)

    def notify_observers(self, data, connection):
        for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_kick, (observer, data, connection))
