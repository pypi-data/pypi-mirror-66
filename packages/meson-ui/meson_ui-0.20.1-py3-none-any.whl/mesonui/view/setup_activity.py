#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from PyQt5.QtWidgets import QMessageBox as SnackBarMessage
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from ..mesonuilib.coredata import MesonUiCache
from ..mesonuilib.coredata import default_core
from ..mesonuilib.coredata import default_base
from ..mesonuilib.coredata import default_test
from ..mesonuilib.coredata import default_path
from ..mesonuilib.coredata import default_backend
from ..mesonuilib.backend import backend_factory
from ..repository.mesonapi import MesonAPI
from ..models.appmodel import MainModel
from ..mesonuitheme import MesonUiTheme
from ..containers.stack import MesonUiStack

from pathlib import Path
import logging

from ..ui.activity_setup import Ui_Activity_Setup_Dialog

MESON_BACKENDS = ['xcode', 'ninja', 'vs2010', 'vs2015', 'vs2017', 'vs2019']


class SetupActivity(QDialog, Ui_Activity_Setup_Dialog):
    '''
    this class is are Setup Activity
    '''
    def __init__(self, console, model: MainModel = None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(MesonUiTheme().set_theme())
        self.setFixedSize(740, 421)

        self._model: MainModel = model
        self._console = console

        self.on_activity_start()
        self.show()

    @pyqtSlot()
    def on_activity_start(self, context=None) -> None:
        '''
        This method is the starting point of this Meson-UI
        and is called after the app is initlzied.
        '''
        self._cache = MesonUiCache()

        self.control_push_no_setup.clicked.connect(lambda: self.exec_no_setup())
        self.control_push_do_setup.clicked.connect(lambda: self.exec_do_setup())
        self.control_push_do_update.clicked.connect(lambda: self.exec_do_update())
        self.meson_api: MesonAPI = MesonAPI(
            self._model.buildsystem().meson().sourcedir,
            self._model.buildsystem().meson().builddir
        )

        self._cache.init_cache()
        self._cache_default()

    @pyqtSlot()
    def exec_no_setup(self):
        '''
        this method will just close are activity
        '''
        logging.info('User quits "meson setup" command')
        self.close()
    # end of method

    @pyqtSlot()
    def exec_do_update(self):
        '''
        this method just calls _cache_update to refresh current settings
        values in configure cache object
        '''
        SnackBarMessage.information(self, 'Saved current settings', 'Your current settings have been saved.')
        self._cache_update()
    # end of method

    @pyqtSlot()
    def exec_do_setup(self):
        '''
        this method will perform the "meson setup" action and pass all
        options with the set whatever the user would like
        '''
        if self._model.buildsystem().meson().builddir != '':
            #
            # here we define are process on how we are
            # going to build a set object with Meson
            # build args.
            meson_args: MesonUiStack = MesonUiStack()

            self._cache_update()
            self._cache_parser(meson_args=meson_args)
            self._cache_sender(meson_args=meson_args)
        #
        # then close are activity
        self.close()

    def _cache_sender(self, meson_args: MesonUiStack) -> None:
        '''
        this method will send the set to are Meson wrapper object
        '''
        logging.info(' Setup Meson project')
        args: list = list()
        for i in range(len(meson_args.stack)):
            args.extend(meson_args.pop())
        if self._console is None:
            return
        else:
            if self.combo_backend.currentText() in MESON_BACKENDS:
                self._console.command_run(str(self._model.buildsystem().meson().setup(args=args)))
            else:
                args.remove(f'--backend={self.combo_backend.currentText()}')
                args.append('--backend=ninja')
                self._console.command_run(str(self._model.buildsystem().meson().setup(args=args)))
                ide = backend_factory(self.combo_backend.currentText(), self.meson_api)
                ide.generator()

    def _cache_parser(self, meson_args: MesonUiStack) -> None:
        '''
        this method will parse the given cache configuration
        via extract from cache objects internal set value and
        add to local 'meson_args' setup
        '''
        #
        # here we need to always get a fresh copy of
        # the current configuration data from are core
        # cache data so we don’t pass old data.
        core: dict = self._cache.get_core()
        base: dict = self._cache.get_base()
        test: dict = self._cache.get_test()
        path: dict = self._cache.get_path()
        back: dict = self._cache.get_backend()
        #
        # here we add Meson core config values from
        # are cache object.
        #
        # here we also check to see if the option is
        # is eithor a 'werror', 'strip' so
        # we don't get an error.  Else we just pass
        # are option name equale to user set value.
        for conf in core:
            if conf in ['--werror', '--strip', '--fatal-meson-warnings']:
                meson_args.push([f'{conf}'])
            else:
                meson_args.push([f'{conf}={core[conf]}'])
        #
        # here we add Meson base config values from
        # are cache object.
        for conf in base:
            meson_args.push([f'{conf}={base[conf]}'])
        #
        # here we add Meson test config values from
        # are cache object.
        for conf in test:
            meson_args.push([f'{conf}'])
        #
        # here we add Meson directory config values from
        # are cache object.
        for conf in path:
            meson_args.push([f'{conf}={path[conf]}'])
        #
        # here we add Meson backend config values from
        # are cache object.
        for conf in back:
            meson_args.push([f'{conf}={back[conf]}'])
        #
        # here we wipe the current builddir if it exists and start new
        if Path(self._model.buildsystem().meson().builddir).exists():
            meson_args.push(['--wipe'])

    def _cache_update(self) -> None:
        '''
        this method will update all supported Meson build options
        to whatever the user sets the values to.
        '''
        #
        # Meson args passed for (Core options)
        self._cache.configure_core('fatal-meson-warnings', self.combo_fetal_warnings.currentText())
        self._cache.configure_core('auto-features',     self.combo_auto_features.currentText())
        self._cache.configure_core('backend',           self.combo_backend.currentText())
        self._cache.configure_core('buildtype',         self.combo_buildtype.currentText())
        self._cache.configure_core('default-library',   self.combo_default_library.currentText())
        self._cache.configure_core('layout',            self.combo_layout.currentText())
        self._cache.configure_core('unity',             self.combo_unity.currentText())
        self._cache.configure_core('warnlevel',         self.combo_warnlevel.currentText())
        self._cache.configure_core('wrap-mode',         self.combo_wrap_mode.currentText())
        self._cache.configure_core('werror',            self.combo_werror.currentText())
        self._cache.configure_core('strip',             self.combo_strip.currentText())
        self._cache.configure_core('cmake-prefix-path', self.edit_cmake_prefix_path.text())
        self._cache.configure_core('pkg-config-path',   self.edit_pkg_config_path.text())
        #
        # Meson args passed for (Base options)
        self._cache.configure_base('b_colorout',  self.combo_b_colorout.currentText())
        self._cache.configure_base('b_coverage',  self.combo_b_coverage.currentText())
        self._cache.configure_base('b_lundef',    self.combo_b_lundef.currentText())
        self._cache.configure_base('b_ndebug',    self.combo_b_ndebug.currentText())
        self._cache.configure_base('b_lto',       self.combo_b_lto.currentText())
        self._cache.configure_base('b_pch',       self.combo_b_pch.currentText())
        self._cache.configure_base('b_pgo',       self.combo_b_pgo.currentText())
        self._cache.configure_base('b_pie',       self.combo_b_pie.currentText())
        self._cache.configure_base('b_sanitize',  self.combo_b_sanitize.currentText())
        self._cache.configure_base('b_staticpic', self.combo_b_staticpic.currentText())
        self._cache.configure_base('b_vscrt',     self.combo_b_vscrt.currentText())
        #
        # Meson args passed for (Directory options)
        self._cache.configure_path('prefix',         self.edit_prexif.text())
        self._cache.configure_path('bindir',         self.edit_bindir.text())
        self._cache.configure_path('datadir',        self.edit_datadir.text())
        self._cache.configure_path('includedir',     self.edit_includedir.text())
        self._cache.configure_path('infodir',        self.edit_infodir.text())
        self._cache.configure_path('libdir',         self.edit_libdir.text())
        self._cache.configure_path('libexecdir',     self.edit_libexecdir.text())
        self._cache.configure_path('localedir',      self.edit_localedir.text())
        self._cache.configure_path('localstatedir',  self.edit_localstatedir.text())
        self._cache.configure_path('mandir',         self.edit_mandir.text())
        self._cache.configure_path('sbindir',        self.edit_sbindir.text())
        self._cache.configure_path('sharedstatedir', self.edit_sharedstatedir.text())
        self._cache.configure_path('sysconfdir',     self.edit_sysconfdir.text())
        #
        # Meson args passed for (Backend options) # --backend_max_links=0
        self._cache.configure_backend('backend_max_links',  self.edit_backend_max_links.text())
        #
        # Meson args passed for (Test options)
        self._cache.configure_test('errorlogs', self.combo_errorlogs.currentText())
        self._cache.configure_test('stdsplit',  self.combo_stdsplit.currentText())

    def _cache_default(self) -> None:
        '''
        here we set all supported options to the first value
        from are default cache settings dict objects.
        '''
        #
        # Meson args passed for (Core options)
        self.combo_fetal_warnings.addItems(default_core['fatal-meson-warnings'])
        self.edit_cmake_prefix_path.setText(default_core['cmake-prefix-path'])
        self.edit_pkg_config_path.setText(default_core['pkg-config-path'])
        self.combo_default_library.addItems(default_core['default-library'])
        self.combo_auto_features.addItems(default_core['auto-features'])
        self.combo_buildtype.addItems(default_core['buildtype'])
        self.combo_warnlevel.addItems(default_core['warnlevel'])
        self.combo_wrap_mode.addItems(default_core['wrap-mode'])
        self.combo_backend.addItems(default_core['backend'])
        self.combo_werror.addItems(default_core['werror'])
        self.combo_strip.addItems(default_core['strip'])
        self.combo_unity.addItems(default_core['unity'])
        self.combo_layout.addItems(default_core['layout'])
        #
        # Meson args passed for (Base options)
        self.combo_b_colorout.addItems(default_base['b_colorout'])
        self.combo_b_coverage.addItems(default_base['b_coverage'])
        self.combo_b_lundef.addItems(default_base['b_lundef'])
        self.combo_b_ndebug.addItems(default_base['b_ndebug'])
        self.combo_b_lto.addItems(default_base['b_lto'])
        self.combo_b_pch.addItems(default_base['b_pch'])
        self.combo_b_pgo.addItems(default_base['b_pgo'])
        self.combo_b_pie.addItems(default_base['b_pie'])
        self.combo_b_vscrt.addItems(default_base['b_vscrt'])
        self.combo_b_sanitize.addItems(default_base['b_sanitize'])
        self.combo_b_staticpic.addItems(default_base['b_staticpic'])
        #
        # Meson args passed for (Directory options)
        self.edit_includedir.setText(default_path['includedir'])
        self.edit_libexecdir.setText(default_path['libexecdir'])
        self.edit_infodir.setText(default_path['infodir'])
        self.edit_libdir.setText(default_path['libdir'])
        self.edit_prexif.setText(default_path['prefix'])
        self.edit_mandir.setText(default_path['mandir'])
        self.edit_bindir.setText(default_path['bindir'])
        self.edit_sbindir.setText(default_path['sbindir'])
        self.edit_datadir.setText(default_path['datadir'])
        self.edit_localedir.setText(default_path['localedir'])
        self.edit_sysconfdir.setText(default_path['sysconfdir'])
        self.edit_sysconfdir.setText(default_path['sysconfdir'])
        self.edit_localstatedir.setText(default_path['localstatedir'])
        self.edit_sharedstatedir.setText(default_path['sharedstatedir'])
        #
        # Meson args passed for (Backend options)
        self.edit_backend_max_links.setText(default_backend['backend_max_links'])
        #
        # Meson args passed for (Test options)
        self.combo_errorlogs.addItems(default_test['errorlogs'])
        self.combo_stdsplit.addItems(default_test['stdsplit'])
