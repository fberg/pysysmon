# -*- coding: utf-8 -*-

import os.path

from pysysmon.util import Monitor

class HwMon (Monitor):
    """
    Displays the output of a hardware monitoring device
    """

    TEMP = "temp"
    FAN = "fan"
    IN = "in"

    def __init__(self, **args):
        self._device = "hwmon0"
        self._sensor_type = HwMon.TEMP
        self._sensor_id = 1
        self._format = '%.1f'

        Monitor.__init__(self, **args)

    def execute(self):
        _hwmon_dir = "/sys/class/hwmon/"

        _hwmon_file = _hwmon_dir + self._device + '/' + \
            self._sensor_type + str(self._sensor_id) + '_input'

        if os.path.exists(_hwmon_file):
            with open(_hwmon_file, 'r') as hwmon_file:
                value = hwmon_file.readline().strip()

            value = int(value)

            if self._sensor_type == HwMon.TEMP:
                value /= 1000.0

            return self._format % value

        return None
