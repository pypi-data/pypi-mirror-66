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

from ..mesonuilib.coredata import MesonUiInstallCache
from ..mesonuilib.coredata import default_install
from ..models.appmodel import MainModel
from ..mesonuitheme import MesonUiTheme

import typing as T

from ..ui.activity_install import Ui_Activity_Dist_Dialog


class InstallActivity(QDialog, Ui_Activity_Dist_Dialog):
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
        self._cache: MesonUiInstallCache = MesonUiInstallCache()

        self.control_push_do_update.clicked.connect(lambda: self.exec_do_update())
        self.control_push_do_install.clicked.connect(lambda: self.exec_do_dist())
        self.control_push_no_install.clicked.connect(lambda: self.exec_no_dist())

        self._cache.init_cache()
        self._cache_default()

    @pyqtSlot()
    def exec_do_dist(self):
        '''
        this method will perform the "meson install" action and pass all
        options with the set whatever the user would like
        '''
        meson_args: list = list()

        self._cache_update()
        self._cache_parser(meson_args=meson_args)
        self._cache_sender(meson_args=meson_args)

        self.close()

    @pyqtSlot()
    def exec_do_update(self):
        '''
        this method just calls _cache_update to refresh current settings
        values in configure cache object
        '''
        self._cache_update()

    @pyqtSlot()
    def exec_no_dist(self):
        self.close()

    def _cache_sender(self, meson_args: list) -> None:
        '''
        this method will send the set to are Meson wrapper object
        '''
        self._meson.install(meson_args)

    def _cache_parser(self, meson_args: list) -> None:
        '''
        this method will parse the given cache configuration
        via extract from cache objects internal set value and
        add to local 'meson_args' setup
        '''
        #
        # here we need to always get a fresh copy of
        # the current configuration data from are core
        # cache data so we don’t pass old data.
        cache: T.Dict = self._cache.get_cache()
        #
        # here we add Meson install config values from
        # are cache object.
        for conf in cache:
            meson_args.extend([f'{conf}={cache[conf]}'])

    def _cache_update(self) -> None:
        '''
        this method will update all supported Meson build options
        to whatever the user sets the values to.
        '''
        self._cache.configure('formats',             self.combo_formats.currentText())
        self._cache.configure('include-subprojects', self.combo_include_subprojects.currentText())
        self._cache.configure('quiet', self.combo_include_subprojects.currentText())

    def _cache_default(self) -> None:
        '''
        here we set all supported options to the first value
        from are default cache settings dict objects.
        '''
        self.combo_no_rebuild.addItems(default_install['on-rebuild'])
        self.combo_only_changed.addItems(default_install['only-changed'])
        self.combo_quiet.addItems(default_install['quiet'])
