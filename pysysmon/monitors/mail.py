# -*- coding: utf-8 -*-

import os
import os.path

from pysysmon.util import Monitor

class NewMailCount (Monitor):
    """
    Returns the total count of all new mails in the mailboxes specified by 'mailboxes'.
    """

    def __init__(self, **args):
        self._base_dir = os.path.expanduser("~/Mail")
        self._mailboxes = ["INBOX"]
        self._new_mail_wrap = []

        Monitor.__init__(self, **args)

    def execute(self):
        count = 0

        for mailbox in self._mailboxes:
            path = self._base_dir + '/' + mailbox + '/new'
            if os.path.exists(path):
                count += len(os.listdir(path))

        if count == 0:
            return None
        else:
            return self._new_mail_wrap[0] + str(count) + self._new_mail_wrap[1]

class NewMailCountDetailed (Monitor):
    """
    Gives a string in the form '<mailbox_name>[<new_mail_count>]'.
    """

    def __init__(self, **args):
        self._base_dir = os.path.expanduser("Mail")
        self._mailboxes = ["INBOX"]
        self._new_mail_wrap = []

        Monitor.__init__(self,**args)

    def execute(self):
        counts = dict()

        output = None

        for mailbox in self._mailboxes:
            path = self._base_dir + '/' + mailbox + '/new'
            if os.path.exists(path):
                counts[mailbox] = len(os.listdir(path))

                if counts[mailbox] != 0:
                    if output:
                        output += " "
                    else:
                        output = ""

                    output += mailbox + "[" + str(counts[mailbox]) + "]"

        if output:
            return self._new_mail_wrap[0] + output + self.new_mail_wrap[1]
