class RemoteUser(object):
    """
    Holds information about another user on IRC (nick!user@host)
    """

    def __init__(self, nick, user, host):
        self.nick = nick
        self.user = user
        self.host = host
