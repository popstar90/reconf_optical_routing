class Empty:
    """
    Class d'exception personnalisée
    """
    def __init__(self, delta):
        self.__delta = delta

    @property
    def delta(self):
        """
        Getter au sens python
        :return:
        """
        return self.__delta
