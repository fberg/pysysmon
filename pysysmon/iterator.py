# -*- coding: utf-8 -*-
import copy
import re

from .util import Monitor

class Iterator (Monitor):

    def __init__(self, **args):
        self._template = ''
        self._separator = ' '
        self._monitors = {}
        self._iter_var = '%ITER%'
        self._iterator = None

        Monitor.__init__(self, **args)

        self.regex = None

    def collect_arguments(self):
        raise NotImplementedError(
            "collect_arguments() method nees to be implemented by subclass"
        )       

    def replace_recursive(self, obj, iter_var, repl):
        if hasattr(obj, '__dict__'):
            for key, val in obj.__dict__.items():

                #replace string values
                if type(val) == str and type(self._iter_var) == str and self._iter_var in val:
                    if not self.regex:
                        self.regex = re.compile(self._iter_var)
                    obj.__dict__[key] = self.regex.sub(repl, val)
                
                # replace integer values
                if type(val) == int and self._iter_var == val:
                    obj.__dict__[key] = repl

                if hasattr(obj.__dict__[key], '__dict__'):
                    self.replace_recursive(obj.__dict__[key], iter_var, repl)

    def execute(self):
        output = ""

        if self._iterator:
            args = self._iterator
        else: args = self.collect_arguments()

        for arg in args:
            monitors = copy.deepcopy(self._monitors)

            for id, monitor in monitors.items():
                self.replace_recursive(monitor, self._iter_var, arg)
                monitors[id] = monitor

            output += self._template.format(
                **dict([(key, repr(val)) for key, val in monitors.items()])
            ) + self._separator

        if len(output) == 0:
            return None

        #print "OUT:", output

        # cut off the last separator
        return output[0:len(output)-len(self.separator)]
