import _thread
import queue
import socket
import time
from threading import Condition

from FaustBot.Communication.JoinObservable import JoinObservable
from FaustBot.Communication.KickObservable import KickObservable
from FaustBot.Communication.LeaveObservable import LeaveObservable
from FaustBot.Communication.MagicNumberObservable import MagicNumberObservable
from FaustBot.Communication.NickChangeObservable import NickChangeObservable
from FaustBot.Communication.NoticeObservable import NoticeObservable
from FaustBot.Communication.PingObservable import PingObservable
from FaustBot.Communication.PrivmsgObservable import PrivmsgObservable
from FaustBot.Model.ConnectionDetails import ConnectionDetails
from FaustBot.StringBuffer import StringBuffer


class Connection(object):
    send_queue = queue.Queue()
    details = None
    irc = None

    def sender(self):
        while True:
            msg = self.send_queue.get()
            if msg[-1] != b'\n':
                msg = msg + b'\n'
            self.irc.send(msg)
            time.sleep(1)

    def send_channel(self, text):
        """
        Send to channel
        :return:
        """
        self.raw_send("PRIVMSG " + self.details.get_channel() + " :" + text[0:])

    def send_to_user(self, user, text):
        """
        Send to user
        :return:
        """
        self.raw_send('PRIVMSG ' + user + ' :' + text)

    def send_back(self, text, data):
        """
        Send message to the channel the command got received in
        :param message:
        :param data: needed because of concurrency, there can't be a global variable holding where messages came from
        :return:
        """
        if data['channel'] == self.details.get_nick():
            self.send_to_user(data['nick'], text)
        else:
            self.send_channel(text)

    def raw_send(self, message):
        self.send_queue.put(message.encode() + '\r\n'.encode())

    def receive(self):
        """
        receive from Network
        """
        try:
            data = self.irc.recv(4096)
            if len(data) == 0:
                return False
        except socket.timeout:
            return False
        data = data.decode('UTF-8', errors='replace')
        #print('received: \n' + data)
        data_lines = self._receiver_buffer.append(data)
        if data is None:
            return False
        # print('splited: ')
        for data in data_lines:
            # print(data)
            data = data.rstrip()
            self.data = data

            splited = data.split(' ')
            if not len(splited) >= 2:
                continue
            command = splited[1]
            #         print(command)
            if data.split(' ')[0] == 'PING':
                self.ping_observable.input(data, self)
            elif command == 'JOIN':
                self.join_observable.input(data, self)
            elif command == 'PART' or command == 'QUIT':
                self.leave_observable.input(data, self)
            elif command == 'KICK':
                self.kick_observable.input(data, self)
            elif command == 'NICK':
                self.nick_change_observable.input(data, self)
            elif command == 'NOTICE':
                self.notice_observable.input(data, self)
            elif command == 'PRIVMSG':
                self.priv_msg_observable.input(data, self)
            else:
                try:
                    int(command)
                    self.magic_number_observable.input(data, self)
                except Exception:
                    pass

        return True

    def is_idented(self, user: str):
        self.send_to_user('NickServ', 'ACC ' + user)
        with self.condition_lock:
            while user not in self.idented_look_up:
                self.condition_lock.wait()
            is_idented = self.idented_look_up[user]
            del self.idented_look_up[user]
            return is_idented

    def is_op(self, user):
        """
        Checks wether the given user is an op in this connections' channel or not.
        :param user: the user to check
        :return: return true if the user is an op, else false
        """
        # add call to raw send with WHO
        # manualy receive data until answer received
        # then evaluate and return
        # this way we'll block the bot until is_op is finished
        return False

    def last_data(self):
        return self.data

    def establish(self):
        """
        establish the connection
        """
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.irc.connect((self.details.get_server(), self.details.get_port()))
        #print(self.irc.recv(512))
        self.irc.send("NICK ".encode() + self.details.get_nick().encode() + "\r\n".encode())
        self.irc.send("USER botty botty botty :Botty \n".encode())
        self.irc.send("JOIN ".encode() + self.details.get_channel().encode() + '\r\n'.encode())
        self.irc.send("WHO ".encode() + self.details.get_channel().encode() + '\r\n'.encode())
        self.irc.send("MODE ".encode()+self.details.get_nick().encode()+" -R".encode()+'\r\n'.encode())
        if (self.details.get_pwd() != ''):
            self.send_to_user("NICKSERV","identify "+self.details.get_nick()+" " +self.details.get_pwd()+' ')

        _thread.start_new_thread(self.sender, ())

    def __init__(self, set_details: ConnectionDetails):
        self.details = set_details
        self.ping_observable = PingObservable()
        self.priv_msg_observable = PrivmsgObservable()
        self.join_observable = JoinObservable()
        self.leave_observable = LeaveObservable()
        self.kick_observable = KickObservable()
        self.nick_change_observable = NickChangeObservable()
        self.notice_observable = NoticeObservable()
        self.magic_number_observable = MagicNumberObservable()
        self.condition_lock = Condition()
        self.idented_look_up = {}
        self.data = None
        self._receiver_buffer = StringBuffer()
