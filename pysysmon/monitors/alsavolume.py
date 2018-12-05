# -*- coding: utf-8 -*-

import re
import subprocess

from pysysmon.util import Monitor, Util

class AlsaVolume (Monitor):
    """
    Displays the volume of an ALSA device's control
    """

    def __init__(self, **args):
        self._control = "PCM"
        self._mute_output = "Mute"
        self._amixer_command = 'amixer'
        self._format = '%3d'
        self._show_units = True

        Monitor.__init__(self, **args)

    def execute(self):
        args = ["sget", self._control]

        amixer_output = Util.execute_shell_process(self._amixer_command, args)

        regex_mute = r'\[off\]'
        regex_vol = r'\d{1,3}%'

        if re.search(regex_mute, amixer_output):
            return self._mute_output

        value = int(re.findall(regex_vol, amixer_output)[0].strip('%'))

        if self._show_units:
            return self._format % value + '%'
        else:
            return self._format % value
