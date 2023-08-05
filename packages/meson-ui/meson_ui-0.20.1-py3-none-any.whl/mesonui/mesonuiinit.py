#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from PyQt5.QtWidgets import QApplication
from .models.appmodel import MainModel
from .view import main_activity
import logging


class MesonUiApplication(QApplication):
    def __init__(self, sys_argv):
        super(self.__class__, self).__init__(sys_argv)
        self._model = MainModel()

    def runner_start(self):
        logging.info(' Init Meson-UI Application runner')
        self.activity = main_activity.MainActivity(self._model)
        self.activity.show()
