# -*- coding: utf-8 -*-

from pysysmon.util import Monitor, Util

class Command (Monitor):

    def __init__(self, **args):
        self._command = None
        self._args = []

        Monitor.__init__(self, **args)

    def execute(self):
        if self._command:
            return Util.execute_shell_process(self._command, self._args).strip()
