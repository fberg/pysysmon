# -*- coding: utf-8 -*-
import os
import copy
import logging

from pysysmon.util import Monitor, Util
from pysysmon.iterator import Iterator

def get_mount_point_statistics(mount_point):
    stat = os.statvfs(mount_point)

    info = {
        'Size': stat.f_bsize * stat.f_blocks,
        'Avail': stat.f_bsize * stat.f_bavail
    }
    info['Used'] = info['Size'] - info['Avail']
    if info['Size'] != 0:
        info['UsePercent'] = (info['Used'] * 100) / info['Size']
    else:
        info['UsePercent'] = 100;

    return info

class DiskUsage (Monitor):
    """
    Displays disk usage of the given mount point
    """

    def __init__(self, **args):
        self._mount_point = '/'
        self._layout = "%(Avail)s/%(Size)s"
        self._format = '%.2f'
        self._show_units = True
        self._short_units = True

        Monitor.__init__(self, **args)

    def execute(self):
        mount_file = open('/proc/mounts')

        for line in mount_file:
            if line.split()[1] == self._mount_point:
                break
        else:
            return None

        info = get_mount_point_statistics(self._mount_point)

        for key, value in info.items():
            if key != 'UsePercent':
                info[key] = Util.format_output(value, self._format,
                    self._show_units, self._short_units)

        if self._show_units:
            info['UsePercent'] = str(info['UsePercent']) + '%'

        return self._layout % info

class DiskUsageIterator (Iterator):
    """
    Displays disk usage of all mount points in the given directory.
    """

    def __init__(self, **args):
        self._mount_point_directories = ('/mnt/', '/media/')

        self.mount_points = []

        self.logger = logging.getLogger("PySysMon.Monitor.DiskUsageIterator")
        Iterator.__init__(self, **args)

    def collect_arguments(self):
        mount_points = []
        mount_file = open('/proc/mounts')

        for line in mount_file:
            mounts = line.split()
            for dir in self._mount_point_directories:
                if dir in mounts[1]:
                    if not mounts[1] in self.mount_points:
                        self.logger.info("Found mount point " + mounts[1])
                    mount_points.append(mounts[1])

        self.mount_points = mount_points
        return self.mount_points
