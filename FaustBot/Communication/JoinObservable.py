import _thread

from FaustBot.Communication.Observable import Observable


class JoinObservable(Observable):
    def input(self, raw_data, connection):
        # ":nick!user@host" "JOIN" "#channel"
        # additional ignored arguments are put into "ign". This could be used
        # for http://ircv3.net/specs/extensions/extended-join-3.1.html in the
        # future.
        prefix, cmd, channel, *ign = raw_data.split(' ')
        hostmask = prefix.lstrip(':')
        nick, userhost = hostmask.split('!')
        user, host = userhost.split('@')

        data = {'raw': raw_data, 'nick': nick, 'user': user, 'host': host,
                'channel': channel, 'raw_nick': hostmask}
        self.notify_observers(data, connection)


    def notify_observers(self, data, connection):
        for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_join, (observer, data, connection))
