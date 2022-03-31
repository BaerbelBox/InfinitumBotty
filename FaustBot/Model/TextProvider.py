class TextProvider(object):
    """
    Provides different Texts
    """

    def get_random_fortune(self):
        """
        :return: a random sentence
        """
        return "Das macht Spa�"

    def get_definiton(self, name):
        """

        :param name: name of definition to get
        :return: the definition
        """
        return "Konnte Definition nicht finden"