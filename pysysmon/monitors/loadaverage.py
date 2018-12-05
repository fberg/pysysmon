# -*- coding: utf-8 -*-

import os

from pysysmon.util import Monitor

class LoadAverage (Monitor):
    """
    Displays the three load average values
    """
    
    def __init__(self, **args):
        self._format = '%.2f %.2f %.2f'
        
        Monitor.__init__(self, **args)
        
    def execute(self):
        try:
            loadavg = os.getloadavg()
        except:
            return None
            
        return self._format % loadavg