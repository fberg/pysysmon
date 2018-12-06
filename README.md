# PySysMon

This is a simple Linux system monitoring tool written in Python, and intended to be used in status bars of setups without full desktop enviroments.
I initially wrote this for use with `xmonad` and `dzen`, and the style of configuration is inspired by XMonad, in the sense that the config file is just a Python program that (among other things) instantiates a `pysysmon.PySysMon` object, which makes configuration very flexible.

Most of PySysMon was originally written around 2009 to 2010, in Python 2.x.
I have started porting it to Python 3.x, and my config files as well as the provided examples seem to work fine, but there are probably still some bits of code that do not yet function with Python 3.

Since this was not originally intended to be made public, the code lacks in documentation, although that may change in the future.

## Examples

Configuration examples are found in the [examples](https://github.com/fberg/pysysmon/tree/master/examples) directory.
These are intended to be run directly (be sure to adjust `sys.path` at the start of the file though) or by putting (or symlinking) them to `~/.pysysmon/config.py` and running `pysysmon.py`.

## Screenshots

Some screenshots I found from a few years back:

![](https://github.com/fberg/pysysmon/tree/master/screenshots/1.png)

![](https://github.com/fberg/pysysmon/tree/master/screenshots/2.png)

These are similar to what one gets with the [complex dzen config file](https://github.com/fberg/pysysmon/tree/master/examples/dzen_complex.py).

## Dependencies
The `Network` monitor requires `ifconfig` and `iwconfig` (if WiFi information is needed).

There are special classes that make life easier when using `dzen`, such as creating bars and histograms, see `dzen.py`. Obviously, this requires `dzen` to make sense.

There is now also preliminary support for workspace buttons and window titles of the `i3` window manager in PySysMon, and this requires `i3ipc`.
