# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import logging

from pysysmon.util import Monitor, Util

class NetworkInterfaceDoesntExistError (Exception):

    def __init__(self, iface):
        self.iface = iface

    def __repr__(self):
        return repr(self.iface)

class Network (Monitor):
    """
    Displays current network upload/download rate
    """

    IFACE_ALL = "all"

    NET_DIR='/sys/class/net/'

    def __init__(self, **args):
        self._interface = Network.IFACE_ALL
        self._format = '%6.1f'
        self._layout = '%(DownloadRate)s/%(UploadRate)s'
        self._show_units = True
        self._short_units = True

        Monitor.__init__(self, **args)

        self.previous_data = time.time(), self.get_transferred_data(self.get_interface_list())

    def get_interface_bytes(self, interface):
        try:
            _rx_bytes_file = '/statistics/rx_bytes'
            _tx_bytes_file = '/statistics/tx_bytes'

            with open(Network.NET_DIR + interface + _rx_bytes_file) as rx_file:
                rx_bytes = int(rx_file.readline())

            with open(Network.NET_DIR + interface + _tx_bytes_file) as tx_file:
                tx_bytes = int(tx_file.readline())
        except:
            raise NetworkInterfaceDoesntExistError(interface)

        return rx_bytes, tx_bytes

    def get_transferred_data(self, interfaces):

        bytes = []

        for iface in interfaces:
            bytes.append(self.get_interface_bytes(iface))

        #if self._direction == Network.UPDOWN:
            #total_bytes = [x[0] + x[1] for x in bytes]
        #elif self._direction == Network.UP:
            #total_bytes = [x[1] for x in bytes]
        #else:
            #total_bytes = [x[0] for x in bytes]

        total_rx_bytes = sum([bytes[x][0] for x in range(len(bytes))])
        total_tx_bytes = sum([bytes[x][1] for x in range(len(bytes))])

        return total_rx_bytes, total_tx_bytes

    def get_interface_list(self):
        interfaces = []

        if (self._interface != Network.IFACE_ALL):
            if self._interface in os.listdir(Network.NET_DIR):
                interfaces.append(self._interface)
        else:
            for iface in os.listdir(Network.NET_DIR):
                if iface == 'lo': continue
                interfaces.append(iface)

        return interfaces

    def execute(self):
        interfaces = self.get_interface_list()

        try:
            current_data = time.time(), self.get_transferred_data(interfaces)
        except NetworkInterfaceDoesntExistError as e:
            print("Interface " + e.iface + " disappeared...")
            del interfaces[e.iface]

        if len(interfaces) == 0:
            return None

        info = {
            'DataDownloaded': current_data[1][0],
            'DataUploaded': current_data[1][1],
            'DownloadRate': (current_data[1][0] - self.previous_data[1][0]) / \
                                (current_data[0] - self.previous_data[0]),
            'UploadRate': (current_data[1][1] - self.previous_data[1][1]) / \
                                (current_data[0] - self.previous_data[0])
        }

        #rate = (current_data[1] - self.previous_data[1]) / \
            #(current_data[0] - self.previous_data[0])

        self.previous_data = current_data

        for key, value in info.items():
            info[key] = Util.format_output(value, self._format,
                self._show_units, self._short_units)

        return self._layout % info

class IfUp (Monitor):

    def __init__(self, **args):
        self._interface = 'eth0'
        self._layout_up_addr = 'up, %(addr)s'
        self._layout_up_link = 'up, link detected'
        self._layout_up = 'up'
        self._layout_down = 'down'
        self._ifconfig = '/bin/ifconfig'

        Monitor.__init__(self, **args)

        self.logger = logging.getLogger("PySysMon.Monitor.Network.IfUp")

    def execute(self):
        args = [self._interface]
        try:
            ifconfig_output = Util.execute_shell_process(self._ifconfig, args)
        except IOError:
            self.logger.error("Error executing " + self._ifconfig + " with arguments " + args)

        down = re.findall(r'DOWN')

class Wifi (Monitor):

    def __init__(self, **args):
        self._interface = 'wlan0'
        self._layout_connected_address = '%(essid)s %(quality_pct).0f %(address)s'
        self._layout_connected = '%(essid)s %(quality_pct).0f%%'
        self._layout_disconnected = 'down'
        self._iwconfig = '/sbin/iwconfig'
        self._ifconfig = '/bin/ifconfig'

        Monitor.__init__(self, **args)

        self.logger = logging.getLogger("PySysMon.Monitor.Network.Wifi")

    def execute(self):
        args = [self._interface]

        try:
            iwconfig_output = Util.execute_shell_process(self._iwconfig, args)
            ifconfig_output = Util.execute_shell_process(self._ifconfig, args)
        except IOError:
            self.logger.error("Error executing iwconfig or ifconfig.");
            return None

        regex = {
            'essid': r'ESSID:"(\S*)"',
            'quality': r'Link Quality=(\d*)/(\d*)',
            'frequency': r'Frequency:(\S*)',
            'ap': r'Access Point: (\S*)',
            'rate': r'Bit Rate=(\d*)'
        }

        data = {}

        try:
            for key, val in regex.items():
                m = re.findall(val, iwconfig_output)
                if len(m) > 0:
                    data[key] = re.findall(val, iwconfig_output)[0]

            addr = re.findall(r'inet addr:(\S*)', ifconfig_output)

            if len(addr) > 0:
                data['address'] = addr[0]

            data['quality_pct'] = None
            if 'quality' in data.keys() and data['quality'][1] != 0:
                data['quality_pct'] = 100 * float(data['quality'][0]) / float(data['quality'][1])
            else:
                data['quality_pct'] = 0

            if 'essid' in data.keys():
                if 'address' in data.keys() and self._layout_connected_address:
                    return self._layout_connected_address % data
                if self._layout_connected:
                    return self._layout_connected % data
            else:
                if self._layout_disconnected:
                    return self._layout_disconnected % data
        except TypeError:
            return None
