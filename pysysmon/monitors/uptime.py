# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime

from pysysmon.util import Monitor, Util

class Uptime (Monitor):

    def __init__(self, **args):
        Monitor.__init__(self, **args)

    def execute(self):
        data = open("/proc/uptime", "r").readline().split()

        delta = datetime.fromtimestamp(time.time()) - \
            datetime.fromtimestamp(time.time() - float(data[0]))

        t = Util.seconds_to_time(delta.seconds)

        return "%d days, %dh, %dm" % (delta.days, t.hour, t.minute)
