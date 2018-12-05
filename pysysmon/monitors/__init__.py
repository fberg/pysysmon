# -*- coding: utf-8 -*-

import os
import sys

from .alsavolume import AlsaVolume
from .battery import Battery, SMAPI
from .command import Command
from .cpu import Cpu, CpuIterator
from .date import Date
from .diskusage import DiskUsage, DiskUsageIterator
from .entropy import Entropy
from .filewatch import FileWatch
from .hwmon import HwMon
from .i3 import i3ws, i3FocusedWindow
from .loadaverage import LoadAverage
from .mail import NewMailCount, NewMailCountDetailed
from .memory import Memory
from .misc import PathShortener
#from .mpdclient import MpdClient
from .network import Network, Wifi
from .onlinestatus import OnlineStatus
from .stdinreader import StdinReader
from .uptime import Uptime

__all__ = [
    'AlsaVolume',
    'Battery',
    'Command',
    'Cpu',
    'CpuIterator',
    'Date',
    'DiskUsage',
    'DiskUsageIterator',
    'Entropy',
    'FileWatch',
    'HwMon',
    'i3ws',
    'i3FocusedWindow',
    'LoadAverage',
    'Memory',
    #'MpdClient',
    'Network',
    'NewMailCount',
    'NewMailCountDetailed',
    'OnlineStatus',
    'PathShortener',
    'SMAPI',
    'StdinReader',
    'Uptime',
    'Wifi'
]
