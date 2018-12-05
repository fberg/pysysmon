# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime,timedelta
import math
import subprocess
import logging
from logging.handlers import RotatingFileHandler

class Util(object):

    @classmethod
    def setup_logging(self, logdir=None, scrnlog=True, txtlog=True, loglevel=logging.DEBUG, name=None):
        global logging_initialized
        if not 'logging_initialized' in globals().keys():
            logging_initialized = False

        if not logging_initialized:
            logdir = os.path.expanduser(logdir)

            if not os.path.exists(logdir):
                os.mkdir(logdir)

            log = logging.getLogger('PySysMon')
            log.setLevel(loglevel)

            log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s :: %(message)s")

            if txtlog:
                txt_handler = RotatingFileHandler(os.path.join(logdir, "pysysmon.log"), backupCount=5)
                txt_handler.doRollover()
                txt_handler.setFormatter(log_formatter)
                log.addHandler(txt_handler)
                log.info("Logger initialized.")

            if scrnlog:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(log_formatter)
                log.addHandler(console_handler)

            logging_initialized = True

    @classmethod
    def shorten_binary_values(self, value, short_units):
        suff = (
            (' Byte', 'B'),
            (' KiB',  'K'),
            (' MiB',  'M'),
            (' GiB',  'G'),
            (' TiB',  'T'),
            (' PiB',  'P'),
            (' EiB',  'E')
        )
        cnt = 0
        while value >= 1024:
            value /= 1024.0
            cnt += 1

        return value, suff[cnt][short_units]

    @classmethod
    def format_output(self, value, format='%s', show_units=True,
                      short_units=True):
        val, unit = self.shorten_binary_values(value, short_units)
        fmt = format
        if show_units:
            fmt += '%s'
            return fmt % (val, unit)
        else:
            return fmt % val

    @classmethod
    def seconds_to_time(self, seconds):
        return datetime.time(
            hour = seconds / 3600,
            minute = seconds / 60 % 60,
            second = seconds % 60
        )

    @classmethod
    def hours_to_time(self, hours):
        _hour = math.trunc(hours)
        _minute = math.trunc(hours % 1 * 60)
        _second = math.trunc(hours * 60 % 1 * 60)

        return datetime.time(
            hour = _hour,
            minute = _minute,
            second = _second
        )

    @classmethod
    def minutes_to_time(self, minutes):
        _hour = math.trunc(minutes / 60)
        _minute = math.trunc(minutes % 60)

        return datetime.time(
            hour = _hour,
            minute = _minute
        )

    @classmethod
    def execute_shell_process(self, command, args=None, input=None):

        arglist = [command]
        arglist.extend(args)

        proc = subprocess.run(
            arglist,
            input=(input.encode() if input is not None else None),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # stdin=echo_proc.stdout,
            # stdin=subprocess.PIPE,
#            shell=True,
            close_fds=True
        )

        # if input:
        #     output, error = pipe.communicate(str(input))
        # else:
        #     output, error = pipe.communicate()

        if proc.stderr:
            raise IOError("error occured during command: " + proc.stderr.decode('utf-8'))
#        if error:
#            logger.error("Error occured during command: " + error)
#            raise IOError("Error occured during commadn: " + error)

#        if pipe.returncode != 0:
#            raise IOError("could not execute command: " + str(arglist))

        return proc.stdout.decode('utf-8')

class KwArgsHandler(object):
    """
    Handles keyword arguments on instance generation, to make configuration nicer
    """

    def __init__(self, **args):
        """
        "Public" attributes of subclasses begin (internally) with a underscore.
        This way it's possible to alert users of typos and not supported attributes.

        This method takes all the keyword arguments of a class initialization and
        sets each "underscore variable" accordingly.
        """
        for key, val in args.items():
            if hasattr(self, '_' + key):
                setattr(self, '_' + key, val)
            else:
                raise AttributeError("attribute %s is not supported here" % key)

    def __getattr__(self, name):
        """
        Makes attributes accessible from the outside (i.e. not only in keyword
        arguments during class initialization) even without the leading underscore.
        """
        if '_' + name in self.__dict__:
            name = '_' + name
        try:
            return self.__dict__[name]
        except KeyError:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        """
        See __getattr__()
        """
        if '_' + name in self.__dict__:
            name = '_' + name
        self.__dict__[name] = value

class Monitor (KwArgsHandler):
    """
    Base class for all system monitoring modules.
    Provides _interval and _alternative_text attributes, so every module inheriting
    from it automatically supports those features.
    """
    def __init__(self, **args):
        self._interval = 5
        self._alternative_text = 'N/A'
        self._update_callback = None

        self.__last_execution = None
        self.__state = None

        KwArgsHandler.__init__(self, **args)

    def __execute__(self):
        # if execute() returns None, display alternative text
        ret = self.execute()
        if ret:
            return ret
        return self._alternative_text

    def __repr__(self):
        if self._interval:
            now = datetime.now()

            # Is it time already?
            if not self.__last_execution or \
                    self.__last_execution + timedelta(0, self._interval) <= now:
                self.__state = self.__execute__()
                self.__last_execution = now

            return self.__state
        else:
            return self.__execute__()

    def update_callback(self):
        if self._update_callback:
            self._update_callback()

    def execute(self):
        """
        This method gets called when the output of the monitor is requested
        (e.g. the current CPU utilization).

        If the return value is None, an alternative text is displayed, else the
        output is the return value of __repr__, so it should be a string.
        """
        raise NotImplementedError(
            "execute() method needs to be implemented by subclass"
        )
