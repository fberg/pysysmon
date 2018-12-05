# -*- coding: utf-8 -*-

from pysysmon.util import Monitor, Util

class Memory (Monitor):
    """
    Displays memory information as provided by /proc/meminfo
    """

    def __init__(self, **args):
        self._layout = "%(MemAppUsed)s"
        self._format = '%.2f'
        self._show_units = True
        self._short_units = True

        Monitor.__init__(self, **args)

    def execute(self):
        with open("/proc/meminfo", "r") as memfile:
            values = {}
            for line in memfile:
                values[line.split()[0].strip(":")] = int(line.split()[1])

        values["MemAppUsed"] = values["MemTotal"] - values["MemFree"] - \
                               values["Buffers"] - values["Cached"]
        values["SwapUsed"] = values["SwapTotal"] - values["SwapFree"]
        values["MemUsedPerc"] = values["MemAppUsed"] * 100.0 / values["MemTotal"]
        if values['SwapTotal'] != 0:
            values["SwapUsedPerc"] = values["SwapUsed"] * 100.0 / values["SwapTotal"]
        else:
            values["SwapUsedPerc"] = 0

        for key, value in values.items():
            if key not in ("MemUsedPerc", "SwapUsedPerc"):
                values[key] = Util.format_output(value * 1024, self._format,
                    self._show_units, self._short_units)

        return self._layout % values
