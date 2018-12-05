# -*- coding: utf-8 -*-

from pysysmon.util import Monitor, Util
import i3ipc
from threading import Thread

class i3Monitor (Monitor):
    def __init__(self, **args):
        self.i3 = i3ipc.Connection()
        self.__current_window = None

        Monitor.__init__(self, **args)

        self.i3.on('window', self.on_window_focus)
        self.i3.on('workspace', self.on_workspace_focus)
        Thread(target=self.i3.main, name='i3 helper').start()

    def on_window_focus(self, i3, e):
        pass

    def on_workspace_focus(self, i3, e):
        pass

class i3ws (i3Monitor):

    def __init__(self, **args):
        self._output = None
        self._separator = ' '
        self._format_focused = '*%(name)s*'
        self._format_visible = '_%(name)s_'
        self._format_urgent = '!%(name)s!'
        self._format_hidden = '%(name)s'

        self.__workspaces = None

        i3Monitor.__init__(self, **args)

        self.on_workspace_focus(self.i3, None)

    def on_workspace_focus(self, i3, e):
        self.__workspaces = []

        # find all workspaces on the specified output
        for ws in self.i3.get_workspaces():
            if not self._output or ws['output'] == self._output:
                self.__workspaces.append(ws)

        self.update_callback()

    def execute(self):
        if self.__workspaces:
            out = []
            for w in self.__workspaces:
                if w['focused']:
                    out.append(self._format_focused % w)
                    continue
                if w['visible']:
                    out.append(self._format_visible % w)
                    continue
                if w['urgent']:
                    out.append(self._format_urgent % w)
                    continue
                out.append(self._format_hidden % w)
            return self._separator.join(out)

class i3FocusedWindow (i3Monitor):

    def __init__(self, **args):
        self._output = None
        self._workspace = None
        self._format = '%(name)s'
        self.__current_window = None

        i3Monitor.__init__(self, **args)

    def on_window_focus(self, i3, e):
        # for w in self.i3.get_tree():
            # if w.focused: self.__current_window = w
        if e.container.focused:
            if self._workspace is not None or self._output is not None:
                # check if the focused window belongs to the specified workspace or output
                ws = None
                out = None
                node = self.i3.get_tree().find_by_id(e.container.id)
                if node is None:
                    return

                while node.type != 'root':
                    node = node.parent
                    # if node is not None: return
                    if node.type == 'workspace':
                        if self._workspace and node.name != self._workspace:
                            return
                    if node.type == 'output':
                        if self._output and node.name != self._output:
                            return

            self.__current_window = e.container
        self.update_callback()

    def execute(self):
        if self.__current_window:
            return self._format % self.__current_window.__dict__
