import _thread

from FaustBot.Communication.Observable import Observable


class LeaveObservable(Observable):
    def input(self, raw_data, connection):
        data = {}
        leave_or_part = "PART" if raw_data.find('PART') != -1 else "QUIT"
        data['raw'] = raw_data
        data['nick'] = raw_data.split('!')[0][1:]
        data['channel'] = raw_data.split(leave_or_part + ' ')[1].split(' :')[0]
        data['raw_nick'] = raw_data.split(' ' + leave_or_part)[0][1:]
        self.notify_observers(data, connection)

    def notify_observers(self, data, connection):
        for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_leave, (observer, data, connection))
