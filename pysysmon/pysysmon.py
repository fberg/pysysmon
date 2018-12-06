#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2009-2018, Franz Berger

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import time
import subprocess
import sys
import traceback
import logging

from .util import KwArgsHandler, Util

class PySysMon (KwArgsHandler):
    def __init__(self, **args):
        self._pipe_command = None
        self._interval = 1
        self._run_once = False
        self._name = 'unnamed'
        self._layout = None
        self._separator = " "
        self._print_to_stdout = True
        self._monitors = None
        self._logdir = "~/.pysysmon/logs"

        KwArgsHandler.__init__(self, **args)
        Util.setup_logging(logdir=self._logdir)

        self.logger = logging.getLogger("PySysMon.Core")
        if self._name:
            self.logger.info("Created PySysMon instance '" + self._name + "'")

    def execute(self):
        """
        Runs all the monitors and packs the results in a list/dictionary.
        """
        if type(self._monitors) == dict:
            return dict(
                [(key, repr(mon)) for key, mon in self._monitors.items()]
            )
        if type(self._monitors) == list:
            return [repr(mon) for mon in self._monitors]

    def __repr__(self):
        result = self.execute()

        if type(result) == dict:
            return self._layout.format(**result)
        if type(result) == list:
            return self._separator.join(result)

    def update(self):
        output = repr(self)

        if self._print_to_stdout:
            print(output)
        if self._pipe_command:
            try:
                self.__pipe.stdin.write((output + '\n').encode())
            except IOError:
                self.logger.error("Pipe broken. Exiting.")

    def start(self):
        """
        Starts the system monitor, looping forever and executing its modules
        every <interval> seconds.
        """

        # give a callback handler to every Monitor
        mons = self._monitors if type(self._monitors) == list else self._monitors.values()
        for m in mons:
            m._update_callback = self.update

        if self._pipe_command:
            cmd = self._pipe_command

            if type(self._pipe_command) != list:
                import shlex
                cmd = shlex.split(cmd)

            self.__pipe = subprocess.Popen(
                cmd,
                stdin = subprocess.PIPE,
                bufsize = 0
                # shell = True
            )

        while True:
            try:
                self.update()
                if self._run_once:
                    break
                time.sleep(self._interval)
            except KeyboardInterrupt:
                self.logger.info("Caught keyboard interrupt. Exiting.")
                break

    def start_thread(self):
        """
        Same as start(), but launches a new thread and returns the threading.Thread object.
        """
        from threading import Thread

        self.logger.info("Starting PySysMon instance '" + self._name + "'")
        t = Thread(target=self.start, name=self._name)
        t.start()

        return t
