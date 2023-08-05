#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from .mesonuiinit import MesonUiApplication
from .mesonuilogs import mesonui_log
from .commandline import mesonui_cli
from PyQt5.QtGui import QIcon
import logging
import sys
import os


def mesonui_main():
    mesonui_log()
    mesonui_cli()

    logging.info(' Getting Meson-UI Application started')
    app: MesonUiApplication = MesonUiApplication(sys_argv=sys.argv)

    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), '..', 'graphics', 'meson_app_ic.png')
    app.setWindowIcon(QIcon(path))

    logging.info(' Running Meson-UI Application')
    app.runner_start()
    sys.exit(app.exec_())
