# -*- coding: utf-8 -*-

import socket

from pysysmon.util import Monitor

class OnlineStatus (Monitor):
    """
    Checks if a service on a host is online
    """
    
    def __init__(self, **args):
        self._host = None
        self._port = None
        self._timeout = 0.25
        self._output_success = 'online'
        self._output_failure = 'offline'
        
        Monitor.__init__(self, **args)
        
    def execute(self):
        sock = socket.socket()
        sock.settimeout(self._timeout)
        try:
            sock.connect((self._host, self._port))
            return self._output_success
        except socket.error:
            return self._output_failure