#!/usr/bin/env python3
"""
Copyright 2009-2018, Franz Berger

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pysysmon
import sys
import logging
import os.path
import subprocess

from pysysmon.util import Util

if __name__ == "__main__":
    Util.setup_logging(logdir="/home/frank/.pysysmon")
    logger = logging.getLogger("root")

    config_paths = [
        '~/.pysysmon/pysysmon.py',
        '~/.pysysmon/pysysmon',
        '~/.pysysmon/config.py',
        '~/.pysysmon/config',
        '~/.pysysmon.py'
    ]

    import os.path

    for path in config_paths:
        _config_path = os.path.expanduser(path)

        if os.path.isfile(_config_path):
            logger.info("Using config file " + _config_path)
            ##waits for process
            #retcode = subprocess.call(_config_path)

            # forks to background
            subprocess.run([_config_path])

            break
