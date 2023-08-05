#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
import logging


color = {
    'green': '\x1B[01;32m',
    'blue': '\033[94m',
    'bold': '\033[1m',
    'reset': '\x1B[0m'
}

log_format = (
    f'{color["green"]} cat_log: {color["reset"]}'
    f'{color["blue"]} %(funcName)s - {color["reset"]}'
    f'{color["bold"]} %(message)s {color["reset"]}'
)

#
# NOTE should impl formatters for log types
#
# TODO impl current logger so I can have clean logs.  Good for
#      reading actions Meson-UI runs.
def mesonui_log():
    logging.basicConfig(level=logging.INFO, format=log_format)

#
# TODO impl error logger so I can save issue logs.  Good for
#      finding bugs in Meson-UI.
def init_error_logger():
    pass
