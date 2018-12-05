# -*- coding: utf-8 -*-

import sys
import os
import logging
from pysysmon.util import Monitor, Util

class Battery (Monitor):
    """
    Battery monitor. Supports batteries through /sys/class/power_supply/
    """
    def __init__(self, **args):
        self._battery = "BAT0"
        self._format_all = None
        self._format_discharging = "{charge_percent:.1f}% {time_remaining}"
        self._format_charging = "{charge_percent:.1f}% {time_remaining}"
        self._format_charged = "{charge_percent:.1f}%"
        self._time_format = "%H:%M"

        Monitor.__init__(self, **args)

        # Initialize battery

    @property
    def batdir(self):
        return "/sys/class/power_supply/" + self._battery + "/"

    def execute(self):
        values = {
            # values from /sys
            "status": None,
            "charge_full": None,
            "charge_full_design": None,
            "charge_now": None,
            "current_now": None,
            "status": None,
            "voltage_min_design": None,
            "voltage_now": None,
            # custom values
            "charge_percent": None,
            "time_remaining": None
        }

        for key in values.keys():
            if os.path.exists(self.batdir + key):
                batfile = open(self.batdir + key, "r")
                values[key] = batfile.readline()
                batfile.close()

        charging = "Charging" in values["status"]
        discharging = "Discharging" in values["status"]
        charged = "Unknown" in values["status"]

        if values["charge_now"] and values["charge_full"]:
            values["charge_percent"] = int(values["charge_now"]) * 100 / int(values["charge_full"])

        # calculating remaining time
        time = None

        if values["current_now"]:
            if discharging:
                time = float(values["charge_now"]) / float(values["current_now"])
            elif charging:
                time = (float(values["charge_full"]) - float(values["charge_now"])) / float(values["current_now"])
            if time: values["time_remaining"] = Util.hours_to_time(time).strftime(self._time_format)

        #print values

        if self._format_all:
            return self._format_all.format(**values)

        if charging:
            return self._format_charging.format(**values)
        elif discharging:
            return self._format_discharging.format(**values)
        elif charged:
            return self._format_charged.format(**values)

class SMAPI (Monitor):
    """
    This implements support for SMAPI batteries found in ThinkPad
    computers.
    """
    def __init__(self, **args):
        self._battery = "BAT0"

        self._format_all = None
        self._format_discharging = "%(remaining_percent)s%% %(discharging_time_remaining)s"
        self._format_charging = "%(remaining_percent)s%% %(charging_time_remaining)s"
        self._format_idle = "%(remaining_percent)s"
        self._format_installed = None
        self._format_uninstalled = "No battery"
        self._time_format = "%H:%M"

        Monitor.__init__(self, **args)

        self.batdir = "/sys/devices/platform/smapi/" + self._battery + "/"

        self.logger = logging.getLogger("PySysMon.Monitor.Battery.SMAPI")

    def execute(self):
        values = {}

        for f in os.listdir(self.batdir):
            try:
                batfile = open(self.batdir + f, "r")
                values[f] = batfile.readline().strip()
                batfile.close()
            except IOError:
                self.logger.error("Encountered an error reading battery information from " + self.batdir)
                pass

        values["discharging_time_remaining"] = None
        values["charging_time_remaining"] = None

        if "remaining_running_time_now" in values.keys() and values["remaining_running_time_now"] != "not_discharging":
                values["discharging_time_remaining"] = Util.minutes_to_time(float(values["remaining_running_time_now"]))#.strftime(self._time_format)

        if "remaining_charging_time" in values.keys() and values["remaining_charging_time"] != "not_charging":
                values["charging_time_remaining"] = Util.minutes_to_time(float(values["remaining_charging_time"]))#.strftime(self._time_format)

        try:

            if self._format_all:
                return self._format_all % values

            if values["installed"] == "1":
                if self._format_installed:
                    return self._format_installed % values
                elif values["state"] == "discharging":
                    return self._format_discharging % values
                elif values["state"] == "charging":
                    return self._format_charging % values
                else:
                    return self._format_idle % values

            else:
                return self._format_uninstalled % values
        except KeyError:
            print("KEY ERROR:")
            print(values)
            return None
