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

from ..mesonuilib.coredata import MesonUiInitCache
from ..mesonuilib.coredata import default_init
from ..models.appmodel import MainModel
from ..mesonuitheme import MesonUiTheme

import typing as T
import logging

from ..ui.activity_init import Ui_Activity_Init_Dialog

BLACK_LIST_CHARS = ('', ' ', '\n', '\t')

class InitActivity(QDialog, Ui_Activity_Init_Dialog):
    '''
    this class is are Setup Activity
    '''
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
        self._cache = MesonUiInitCache()

        self.control_push_do_update.clicked.connect(lambda: self.exec_do_update())
        self.control_push_do_init.clicked.connect(lambda: self.exec_do_init())
        self.control_push_no_init.clicked.connect(lambda: self.exec_no_init())

        self._cache.init_cache()
        self._cache_default()

    @pyqtSlot()
    def exec_do_init(self):
        '''
        this method will perform the "meson init" action and pass all
        options with the set whatever the user would like
        '''
        meson_args: list = list()

        self._cache_update()
        self._cache_parser(meson_args=meson_args)
        self._cache_sender(meson_args=meson_args)

        self.close()
    # end of method

    @pyqtSlot()
    def exec_do_update(self):
        '''
        this method just calls _cache_update to refresh current settings
        values in configure cache object
        '''
        self._cache_update()
    # end of method

    @pyqtSlot()
    def exec_no_init(self):
        self.close()
    # end of method

    def _cache_sender(self, meson_args: list) -> None:
        '''
        this method will send the set to are Meson wrapper object
        '''
        for i in meson_args:
            logging.info(f'{i}')
        self._model.buildsystem().meson().init(meson_args)

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
        # here we add Meson init config values from
        # are cache object.
        #
        # here we also check to see if the option is
        # is eithor a '', ' ', '\n', '\t' so we don't
        # get an error.
        for conf in cache:
            if self.edit_version.text() == '' or cache['--version'] == BLACK_LIST_CHARS:
                continue
            if self.edit_name.text() == '' or cache['--name'] in BLACK_LIST_CHARS:
                continue
            meson_args.extend([f'{conf}={cache[conf]}'])

    def _cache_update(self) -> None:
        '''
        this method will update all supported Meson build options
        to whatever the user sets the values to.
        '''
        self._cache.configure('version',  self.edit_version.text())
        self._cache.configure('type',     self.combo_type.currentText())
        self._cache.configure('language', self.combo_lang.currentText())
        self._cache.configure('name',     self.edit_name.text())

    def _cache_default(self) -> None:
        '''
        here we set all supported options to the first value
        from are default cache settings dict objects.
        '''
        self.edit_version.setText(default_init['version'])
        self.combo_type.addItems(default_init['type'])
        self.combo_lang.addItems(default_init['language'])
        self.edit_name.setText(default_init['name'])
