# -*- coding: utf-8 -*-

import time

from pysysmon.util import Monitor

class Date (Monitor):
    """
    Displays the current date and/or time
    """
    
    def __init__(self, **args):        
        self._format = "%F %T"
        # Display a float with the number of kiloseconds elapsed since 00:00:00
        # format won't matter in this case
        self._kiloseconds = False
            
        Monitor.__init__(self, **args)
    
    def execute(self):
        if self._kiloseconds:
            tm = time.localtime()
            return "%.3f" % ((tm.tm_hour*3600 + tm.tm_min*60 + tm.tm_sec) / 1000.0,)
        else:
            return time.strftime(self._format)
