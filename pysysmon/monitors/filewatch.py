# -*- coding: utf-8 -*-

import os

from pysysmon.util import Monitor

class FileWatch (Monitor):

    ALL_LINES = 'all_lines'

    def __init__(self, **args):
        self._file_name = None
        self._lines = FileWatch.ALL_LINES
        self._line_separator = '\n'

        Monitor.__init__(self, **args)

        self.state = ''
        #self.input_file = open(os.path.expanduser(self._file_name))

    def execute(self, **args):
        if not self._file_name:
            return None

        #if not os.path.isfile(self._file_name):
            #return None

        #self.state = ''

        if len(self.state) == 0:
            _file = open(os.path.expanduser(self._file_name))
            for line in _file:
                self.state += line.strip() + self._line_separator

        return self.state.strip()
