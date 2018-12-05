#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.append(os.path.expanduser('~/Store/Applications/pysysmon'))

from pysysmon.util import Util
from pysysmon import PySysMon
from pysysmon.monitors import *
from pysysmon.dzen import *

icon_path = os.path.expanduser("~/.dzen2/icons/")

font = "-*-profont-*-*-*-*-11-*-*-*-*-*-*-*"
DZEN_HEIGHT = 15
common_opts = "-y -1 -h %s -fn '%s'" % (DZEN_HEIGHT, font)
cmd = "/usr/bin/dzen2 -xs 1 -ta r -expand l " + common_opts

PySysMon(
    pipe_command = cmd,
    print_to_stdout = False,
    separator=" ^r(1x{}) ".format(DZEN_HEIGHT),
    monitors = [
        Battery(
            battery='BAT0'
        ),
        Wifi(
            interface='wlp2s0',
            ifconfig='/sbin/ifconfig',
        ),
        Cpu(),
        HwMon(
            device='hwmon0',
            sensor_type=HwMon.TEMP,
            sensor_id=1,
        ),
        Memory(
            layout='MEM %(MemAppUsed)5s SWP %(SwapUsedPerc).1f%%'
        ),
        Network(
            interface='enp0s25',
            format='%4.0f',
            alternative_text="no network"
        ),
        Date(
            format="%a, %F %T"
        )
    ]
).start()
