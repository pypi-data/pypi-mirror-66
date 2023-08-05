#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from ..models.appmodel import MainModel
from ..mesonuitheme import MesonUiTheme
from ..mesonuilib.outputconsole import OutputConsole

from ..ui.activity_subprojects import Ui_Activity_Wrap_Dialog


class SubprojectsActivity(QDialog, Ui_Activity_Wrap_Dialog):
    def __init__(self, model: MainModel = None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(MesonUiTheme().set_theme())
        self.setFixedSize(740, 421)

        self._model: MainModel = model

        self.on_activity_start()
        self.show()

    @pyqtSlot()
    def on_activity_start(self):
        '''
        This method is the starting point of this Meson-UI
        and is called after the app is initlzied.
        '''
        self.control_push_download.clicked.connect(lambda: self.exec_download())
        self.control_push_checkout.clicked.connect(lambda: self.exec_checkout())
        self.control_push_update.clicked.connect(lambda: self.exec_update())
        self.control_push_ok.clicked.connect(lambda: self.exec_ok())
        #
        # All things needed to run Console and list view
        self.console = OutputConsole(self)

    @pyqtSlot()
    def exec_download(self):
        self.console.command_run(self._model.buildsystem().meson().subprojects().download(self.edit_wrap_item.text()))

    @pyqtSlot()
    def exec_checkout(self):
        self.console.command_run(
            self._model.buildsystem().meson().subprojects().checkout(self.entry_branch_item.text(), self.edit_wrap_item.text()))

    @pyqtSlot()
    def exec_update(self):
        self.console.command_run(self._model.buildsystem().meson().subprojects().update(self.edit_wrap_item.text()))

    @pyqtSlot()
    def exec_ok(self):
        self.close()
