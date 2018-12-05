# -*- coding: utf-8 -*-

from pysysmon.util import Monitor

class Entropy (Monitor):
    """
    Displays available kernel entropy (for crypto freaks)
    """

    def __init__(self, **args):
        self._format = '%4d'

        Monitor.__init__(self, **args)

    def execute(self):
        _entropy_file_name = "/proc/sys/kernel/random/entropy_avail"

        try:
            entropy_file = open(_entropy_file_name)
            value = int(entropy_file.readline().strip())
            entropy_file.close()
        except:
            return None

        return self._format % value
