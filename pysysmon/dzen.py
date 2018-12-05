# -*- coding: utf-8 -*-

from .util import Monitor, Util
import math
import subprocess
from functools import reduce

class DzenBar (Monitor):
    """
    Creates a dzen bar from the embedded Monitor.
    """

    # styles
    DEFAULT = ""
    OUTLINED = "o"
    VERTICAL = "v"
    PIE = "p"

    def __init__(self, **args):
        self._monitor = None
        self._value = None
        self._none_to_zero = False
        self._width = 80
        self._height = 10
        self._fgcolors = ((0, "green"), (35, "yellow"), (70, "red"))
        self._bgcolor = "darkgrey"

        self._style = DzenBar.DEFAULT
        self._segmented = False
        self._segment_size = 1
        self._segment_spacing = 1

        self._gdbar = "gdbar"

        self._alternative_text = None

        Monitor.__init__(self, **args)

    def get_value(self):
        if type(self._value) == int:
            return self._value

        if self._monitor:
            self._monitor.show_units = False
            value = self._monitor.execute()

            #if value:
            try:
                value = float(value)
            except:
                if self._none_to_zero:
                    return 0
                else:
                    return None
            return value
            #else:
            #    return None
        else:
            return None

    def execute(self):
        value = self.get_value()

        if (value == None) and self._alternative_text:
            return self._alternative_text

        return self.draw_bar(value)

    def draw_bar(self, value):
        fgcol = self._fgcolors[0][1]

        for col in self._fgcolors:
            if value >= col[0]:
                fgcol = col[1]

        sw = self._segment_size
        if self._style == DzenBar.VERTICAL:
            sw = self._width

        gdbar_args = [
            "-w", str(self._width),
            "-h", str(self._height),
            "-fg", fgcol,
            "-bg", self._bgcolor,
            "-s", self._style,
            "-sw", str(sw),
            "-nonl"
        ]

        if self._segmented:
            gdbar_args.extend([
                "-ss", str(self._segment_spacing),
                #"-sw", str(sw),
                "-sh", str(self._segment_size)
            ])

        return Util.execute_shell_process(self._gdbar, args=gdbar_args, input=str(value))

"""
Obsolete.
"""
"""
class DzenCpuBar (Monitor):
    def __init__(self, **args):
        self._gcpubar = "gcpubar"
        self._gcpubar_args = None

        Monitor.__init__(self, **args)

    def execute(self):
       return Util.execute_shell_process(self._gcpubar, self._gcpubar_args)
"""

class DzenHistogram (DzenBar):
    """
    Creates a histogram by stringing together DzenBars.
    """
    def __init__(self, **args):
        self._monitor = None
        self._separator = ''
        self._num_bars = 50

        args.setdefault('width', 1)
        args.setdefault('style', DzenBar.VERTICAL)
        args.setdefault('segmented', False)

        DzenBar.__init__(self, **args)

        self.output = [self.initialize() for x in range(self._num_bars)]

    def initialize(self):
        # Initialize with Bars of value 0
        self.value = 0
        ret = DzenBar.execute(self)
        self.value = None
        return ret

    def execute(self):
        if len(self.output) > 0:
            del self.output[0]

        value = DzenBar.get_value(self)

        if not value:
            self.output.append(self.initialize())
            return self.alternative_text
        else:
            self.output.append(self.draw_bar(value))

        return reduce(lambda a,b: a + self.separator + b, self.output)
