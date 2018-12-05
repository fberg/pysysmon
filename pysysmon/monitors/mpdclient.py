# -*- coding: utf-8 -*-

import socket
import logging
from datetime import time
# why doesn't it work if I import it later?
from mpd import MPDClient, ConnectionError
from pysysmon.util import Monitor, Util

class MpdClientWrapper (object):
    """
    This is a context manager that wraps a mpd.MPDClient object and enables it's
    use as

        with MpdClientWrapper(host, port) as client:
            [...]

    It catches both mpd.ConnectionError and socket.error and tries to reconnect
    automatically.

    (host, port) defaults to ('localhost', 6600).
    """

    mpd_client = None

    def __init__(self, host='localhost', port=6600):
        self.host = host
        self.port = port

    def __enter__(self):
        if not MpdClientWrapper.mpd_client:
            MpdClientWrapper.mpd_client = MPDClient()

            try:
                MpdClientWrapper.mpd_client.connect(self.host, self.port)
            except socket.error:
                # return None so that the inner code of the
                # with statement doesn't get executed
                MpdClientWrapper.mpd_client = None

        return MpdClientWrapper.mpd_client

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type == ConnectionError:
            MpdClientWrapper.mpd_client = None
        # Discard all exceptions quietly on exit
        return True

class MpdClient (Monitor):
    """
    Provides access to a Music Player Daemon's status.

    The keys available for the layout string the same as returned by
    python-mpd's MPDClient.currentsong(), i.e.:

        'album', 'albumartist', 'artist',
        'composer', 'date', 'file', 'genre',
        'id', 'pos', 'time', 'title', 'track'

    There are five layout strings: layout, layout_playing, layout_paused,
    layout_stopped and layout_filenameonly.
    layout defaults to "%(artist)s - %(title)s". If one or more of the others
    are specified, they override layout in the respective state (playing,
    paused, stopped).
    """

    def __init__(self, **args):
        self.logger = logging.getLogger("PySysMon.Monitor.MpdClient")
        try:
            from mpd import MPDClient, ConnectionError
        except:
            self.logger.error("Couldn't find module python-mpd")
            raise ImportError("You need python-mpd for the MpdClient module.")

        self._host = 'localhost'
        self._port = 6600
        self._layout = "%(artist)s - %(title)s"
        self._layout_filenameonly = "%(file)s"
        self._layout_playing = None
        self._layout_paused = None
        self._layout_stopped = None
        self._time_format = "%M:%S"

        Monitor.__init__(self, **args)

    def execute(self):
        with MpdClientWrapper(self._host, self._port) as cl:
            status = cl.status()
            data = cl.currentsong()

            if "time" in status.keys():
                elapsed, total = status["time"].split(":")
                # get elapsed time as a datetime.time object
                elapsed = int(elapsed); total = int(total)
                data["elapsedtime"] = Util.seconds_to_time(elapsed).strftime(self._time_format)
                data["totaltime"] = Util.seconds_to_time(total).strftime(self._time_format)

            pattern = None

            if status["state"] == 'play' and self._layout_playing:
                pattern = self._layout_playing
            elif status["state"] == 'pause' and self._layout_paused:
                pattern = self._layout_paused
            elif status["state"] == 'stop' and self.layout_stopped:
                pattern = self._layout_stopped

            if not pattern:
                return self._layout % data
            else:
                try:
                  res = pattern % data
                except KeyError:
                  res = self._layout_filenameonly % data
                return res
