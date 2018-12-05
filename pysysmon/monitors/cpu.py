# -*- coding: utf-8 -*-

import time
import os

from pysysmon.util import Monitor
from pysysmon.iterator import Iterator

class Cpu (Monitor):
    """
    Displays current CPU utilization in percent.
    """

    def __init__(self, **args):
        self._cpu_number = None
        self._format =  '%3.0f'
        self._show_units = True

        Monitor.__init__(self, **args)

        #self.previous_times = self.get_time_list()
        self.previous_times = None

    def get_time_list(self):
        with open("/proc/stat", "r") as stat_file:
            times = ""

            if self._cpu_number != None:
                cpu = "cpu" + str(self._cpu_number)
            else:
                cpu = "cpu"

            for line in stat_file.readlines():
                if cpu in line.split():
                    times = line
                    break

            times = times.split()[1:5]

        for i in range(len(times))  :
            times[i] = int(times[i])

        return times

    def get_time_delta(self):
        x = self.get_time_list()
        y = []
        if self.previous_times:
            for i in range(len(x)):
                y.append(x[i] - self.previous_times[i])
        self.previous_times = x
        return y

    def execute(self):
        dt = self.get_time_delta()
        if sum(dt) > 0:
            cpu_pct = 100 - (dt[len(dt) - 1] * 100.00 / sum(dt))
            #cpu_pct = (100 * sum(dt[:-1])) / sum(dt)
            ret = self._format % cpu_pct
            if self._show_units:
                ret += '%'
            return ret

class CpuIterator (Iterator):

    def __init__(self, **args):
        Iterator.__init__(self, **args)

    def collect_arguments(self):
        return range(len(os.listdir('/sys/class/cpuid/')))

if __name__ == '__main__':
    print(Cpu())
