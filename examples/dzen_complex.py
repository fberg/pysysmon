#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.expanduser('~/Store/Applications/pysysmon'))

from pysysmon.util import Util
from pysysmon import PySysMon
from pysysmon.monitors import *
from pysysmon.dzen import *

icon_path = os.path.expanduser("~/.dzen2/icons/")

font = "-*-profont-*-*-*-*-11-*-*-*-*-*-*-*"
fg = '#93A1A1'
bg = '#073642'

icon_color = '#859900'

# Solarized color scheme
solarized_colors = {
    'fg':           '#93A1A1',
#    'bg':           '#002B36',
    'bg':           '#000000',
    'icon':         '#93A1A1',
    'value':        '#EEE8D5',
    'bar_bg':       '#073642',
    'bar_outline':  '#586E75',
    'bar_colors': [
        (0, "#586E75"),
        (95, "#DC322F")
    ],
    'monochrome_bar_colors': [
        (0, "#586E75")
    ],
    'bat_colors': [
        (0, "#DC322F"),
        (25, "#586E75")
    ],
    'swap_colors': [
        (0,"#DC322F")
    ],
    'box': {'bg': "#073642", 'fg': "#FDF6E3"}
}

# Monokai color scheme
monokai_colors = {
    'fg':           '#acada1',
    'bg':           '#272822',
    'icon':         '#acada1',
    'value':        '#f1ebeb',
    'bar_bg':       '#48483e',
    'bar_outline':  '#48483e',
    'bar_colors': [
        (0, "#8fc029"),
        (60, "#d4c96e"),
        (95, "#dc2566")
    ],
    'monochrome_bar_colors': [
        (0, "#acada1")
    ],
    'bat_colors': [
        (0, "#DC322F"),
        (25, "#586E75")
    ],
    'swap_colors': [
        (0,"#DC322F")
    ],
    'box': {'bg': "#d4c96e", 'fg': "#24241f"},
    'workspaces': {
        'focused': {'bg': '#d4c96e', 'fg': '#24241f'},
        'visible': {'bg': '#48483e', 'fg': '#f1ebeb'},
        'urgent': {'bg': '#dc2566', 'fg': '#f1ebeb'},
        'hidden': {'bg': '#272822', 'fg': '#f1ebeb'}
    }
}

colors = solarized_colors

DZEN_HEIGHT = 15
common_opts = "-y -1 -h %s -fg '%s' -bg '%s' -fn '%s'" % (DZEN_HEIGHT, colors['fg'], colors['bg'], font)

def box(text, border=4, fg=colors['box']['fg'], bg=colors['box']['bg']):
    return "^fg(%(bg)s)^r(%(border)sx%(height)s)^fg()^bg(%(bg)s)^fg(%(fg)s)%(text)s^bg()^fg(%(bg)s)^r(%(border)sx%(height)s)^fg()" % {
        'text': text,
        'border': border,
        'fg': fg,
        'bg': bg,
        'height': DZEN_HEIGHT
    }

# let me insert icons easily
i = lambda x, col=colors['icon']: "^fg(" + col + ")^i(" + icon_path + "%s.xbm)^fg()" % x
# ... and values
v = lambda x: "^fg(" + colors['value'] + ")%s^fg()" % x
# ... and boxes
b = lambda x: box(x)

cmd = "/usr/bin/dzen2 -xs 1 -ta r -expand l " + common_opts

# Determine the number of CPUs
import multiprocessing
NUM_CPUS = multiprocessing.cpu_count()

# I'll split the layout string so it doesn't end up being one big line
layout = "^tw()  %(mail)s  %(battery)s  %(wifi)s  %(cpu)s %(cputemp)s  %(mem)s  %(net)s  %(clock)s" % {
    "battery":  "{batmisc}{bat} {batbar}^fg(" + colors['bar_outline'] + ")^r(2x5)^fg()",
    "wifi":     "{wifi}",
    "cpu":      i('cpu') + " " + v('{cpu}') + " " + "^p(1)".join("{cpu_bar" + str(i) + "}" for i in range(NUM_CPUS)) + "^p(3){cpuhist}",
    "cputemp":  i('temp') + " " + v('{cputemp}'),
    "mem":      i('mem') + " " + v('{mem}') + " {mem_bar}^p(2){swap}",
    "net":      i('net_wired') + " {net}",
    # "vol":      i('spkr_01') + " " + v('{vol}'),
    "clock":    i('clock') + " {date}",
    "mail":     '{mailcnt}'
}

date_format = "%a, %F " + b('%T')

network_layout = v('%(DownloadRate)s') + " " + i('net_down_03') + \
                " " + v('%(UploadRate)s') + " " + i('net_up_03')

system_bar = PySysMon(
    pipe_command = cmd,
    print_to_stdout = False,
    # interval = 5,
    name = "system_bar",
    layout = layout,
    monitors = {
        "batmisc": SMAPI(
            battery='BAT0',
            format_installed='Thresh: %(start_charge_thresh)s-%(stop_charge_thresh)s  %(power_now)smW  ',
            format_uninstalled='',
            alternative_text=''
        ),
        "bat": SMAPI(
            battery='BAT0',
            format_discharging=v('%(remaining_percent)s') + '%% %(discharging_time_remaining)s',
            format_charging=v('%(remaining_percent)s') + '%% %(charging_time_remaining)s ' + i('ac'),
            format_idle=v('%(remaining_percent)s') + '%% ' + i('ac_01')
        ),
        "batbar": DzenBar(
            monitor=SMAPI(
                battery='BAT0',
                format_installed='%(remaining_percent)s'
            ),
            none_to_zero=True,
            width=60,
            height=11,
            style=DzenBar.OUTLINED,
            segmented=False,
            fgcolors=colors['bat_colors'],
            bgcolor=colors['bar_outline']
        ),
        "wifi": Wifi(
            interface='wlp2s0',
            ifconfig='/sbin/ifconfig',
            interval=3,
            alternative_text="",
            layout_connected_address=i('wifi_02',colors['value']) + " %(essid)s",
            layout_connected=i('wifi_02') + " %(essid)s",
            layout_disconnected=i('wifi_02_nosignal')
        ),
        "cpu": Cpu(),
        "cpuhist": DzenHistogram(
            monitor=Cpu(),
            num_bars=80,
            width=1,
            height=DZEN_HEIGHT-3,
            fgcolors=colors['monochrome_bar_colors'],
            bgcolor=colors['bar_bg']
        ),
        **{ # One bar for each CPU
            "cpu_bar" + str(i): DzenBar(
                monitor=Cpu(
                    cpu_number=i
                ),
                width=3,
                height=DZEN_HEIGHT-3,
                style=DzenBar.VERTICAL,
                fgcolors=colors['bar_colors'],
                bgcolor=colors['bar_bg']
            ) for i in range(NUM_CPUS)
        },
        "cputemp": HwMon(
            device='hwmon0',
            sensor_type=HwMon.TEMP,
            sensor_id=1,
            format='%.0fC'
        ),
        "mem": Memory(
            layout=v('%(MemAppUsed)5s')
        ),
        "mem_bar": DzenHistogram(
            monitor=Memory(
                layout="%(MemUsedPerc)s"
            ),
            num_bars=10,
            height=DZEN_HEIGHT-3,
            fgcolors=colors['bar_colors'],
            bgcolor=colors['bar_bg']
        ),
        "swap": DzenBar(
            monitor=Memory(
                layout="%(SwapUsedPerc).1f"
            ),
            width=3,
            height=DZEN_HEIGHT-3,
            style=DzenBar.VERTICAL,
            fgcolors=colors['swap_colors'],
            bgcolor=colors['bar_bg']
        ),
        "net": Network(
            interface='enp0s25',
            format='%4.0f',
            layout=network_layout,
            alternative_text="no network"
        ),
        "date": Date(
            format=date_format
        ),
        "mailcnt": NewMailCountDetailed(
            # base_dir=os.expanduser("~/Mail"),
            mailboxes=['gmail/INBOX'],
            alternative_text="",
        )
    }
).start()
