# -*- coding: utf-8 -*-

from pysysmon.util import Monitor

class PathShortener (Monitor):
    """
    Only displays the last num_dirs directories of a path.
    """

    def __init__(self, **args):
        self._split_char = '/'
        self._path = ''
        self._num_dirs = 1

        Monitor.__init__(self, **args)

    def execute(self):
        dirs = self._path.split(self._split_char)[-self._num_dirs:]

        return reduce(lambda a,b: a + self._split_char + b, dirs)

