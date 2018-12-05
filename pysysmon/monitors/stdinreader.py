# -*- coding: utf-8 -*-

import sys

from pysysmon.util import Monitor

class StdinReader (Monitor):
    """
    Displays the input from sys.stdin.
    
    This monitor can be used to pipe text into PySysMon. Note that this monitor only displays the last line of the input.
    """
    
    def __init__(self, **args):
        Monitor.__init__(self, **args)
        
        self.state = None
        
    def execute(self):
        inp = sys.stdin.readlines()
        
        if len(inp) > 0:
            self.state = inp[len(inp)-1]
        else:
            if not self.state:
                self.state = ''
        
        return self.state.strip()