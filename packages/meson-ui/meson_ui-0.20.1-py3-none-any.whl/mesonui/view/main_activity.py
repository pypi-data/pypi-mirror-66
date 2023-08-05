#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from PyQt5.QtWidgets import QMessageBox as SnackBarMessage
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDir

from .subprojects_activity import SubprojectsActivity
from .install_activity import InstallActivity
from .setup_activity import SetupActivity
from .conf_activity import ConfigureActivity
from .dist_activity import DistActivity
from .init_activity import InitActivity
from .wrap_activity import WrapActivity

from ..repository.mesonapi import MesonAPI
from ..dashboard.appdashboard import IntrospectionDashboard
from ..mesonuilib.outputconsole import OutputConsole
from ..models.appmodel import MainModel
from ..mesonuitheme import MesonUiTheme
from os.path import join
from pathlib import Path
import logging
import typing as T

from ..ui.activity_main import Ui_Activity_Main_Window


class MainActivity(QMainWindow, Ui_Activity_Main_Window):
    def __init__(self, model: MainModel = None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(MesonUiTheme().set_theme())
        self.setFixedSize(857, 643)

        self._model: MainModel = model

        self.on_activity_start()

    def on_activity_start(self):
        '''
        This method is the starting point of this Meson-UI
        and is called after the app is initlzied.
        '''
        #
        #
        # All actions that are use for working with entry values
        self.project_sourcedir.setText(str(self._model.buildsystem().meson().sourcedir))
        self.project_builddir.setText(str(self._model.buildsystem().meson().builddir))
        #
        # All actions that are use for working with entry values
        self.control_push_open_sourcedir.clicked.connect(lambda: self.exec_open())
        self.control_push_clear_sourcedir.clicked.connect(lambda: self.exec_clear())
        #
        # All actions that use Meson commands in the background
        self.control_push_subprojects.clicked.connect(lambda: self.exec_subprojects())
        self.control_push_wraptools.clicked.connect(lambda: self.exec_wrap())
        self.control_push_version.clicked.connect(lambda: self.exec_version())
        self.control_push_install.clicked.connect(lambda: self.exec_install())
        self.control_push_intro.clicked.connect(lambda: self.exec_introspect())
        self.control_push_setup.clicked.connect(lambda: self.exec_setup())
        self.control_push_build.clicked.connect(lambda: self.exec_compile())
        self.control_push_clean.clicked.connect(lambda: self.exec_clean())
        self.control_push_conf.clicked.connect(lambda: self.exec_conf())
        self.control_push_dist.clicked.connect(lambda: self.exec_dist())
        self.control_push_init.clicked.connect(lambda: self.exec_init())
        self.control_push_test.clicked.connect(lambda: self.exec_test())
        #
        # All actions that are use for working with entry values
        self.action_clear_sourcedir.triggered.connect(lambda: self.exec_clear())
        self.action_open_sourcedir.triggered.connect(lambda: self.exec_open())
        #
        # All actions that use Meson commands in the background
        self.actionIssue_for_Meson.triggered.connect(lambda: self.onclick_meson_issue())
        self.actionIssue_for_Meson_UI.triggered.connect(lambda: self.onclick_mesonui_issue())
        self.actionMeson_QnA.triggered.connect(lambda: self.onclick_faqs())
        self.actionMeson_docs.triggered.connect(lambda: self.onclick_docs())

        self.action_meson_subprojects.triggered.connect(lambda: self.exec_subprojects())
        self.action_meson_wraptools.triggered.connect(lambda: self.exec_wrap())
        self.action_meson_version.triggered.connect(lambda: self.exec_version())
        self.action_meson_install.triggered.connect(lambda: self.exec_install())
        self.action_meson_intro.triggered.connect(lambda: self.exec_introspect())
        self.action_meson_setup.triggered.connect(lambda: self.exec_setup())
        self.action_meson_build.triggered.connect(lambda: self.exec_compile())
        self.action_meson_clean.triggered.connect(lambda: self.exec_clean())
        self.action_meson_conf.triggered.connect(lambda: self.exec_conf())
        self.action_meson_dist.triggered.connect(lambda: self.exec_dist())
        self.action_meson_init.triggered.connect(lambda: self.exec_init())
        self.action_meson_test.triggered.connect(lambda: self.exec_test())

        self.action_ninja_version.triggered.connect(lambda: self._model.buildsystem().ninja().version())
        self.action_ninja_install.triggered.connect(lambda: self._model.buildsystem().ninja().install())
        self.action_ninja_build.triggered.connect(lambda: self._model.buildsystem().ninja().build())
        self.action_ninja_clean.triggered.connect(lambda: self._model.buildsystem().ninja().clean())
        self.action_ninja_dist.triggered.connect(lambda: self._model.buildsystem().ninja().dist())
        self.action_ninja_test.triggered.connect(lambda: self._model.buildsystem().ninja().test())

        self.meson_api: MesonAPI = MesonAPI(str(self.get_sourcedir()), str(self.get_builddir()))
        self.console: OutputConsole = OutputConsole(self)
        self.dashboard: IntrospectionDashboard = IntrospectionDashboard(self, self.meson_api)
        self.exec_introspect()

    @pyqtSlot()
    def exec_clear(self):
        logging.info('User cleans the entry values for "sourcedir" and "builddir"')
        self.project_sourcedir.clear()
        self.project_builddir.clear()

    @pyqtSlot()
    def exec_version(self) -> None:
        logging.info('Get version number')
        self.console.command_run(f'meson version {self._model.buildsystem().meson().version()}')

    @pyqtSlot()
    def exec_setup(self) -> None:
        logging.info('Setup project process')
        self._model.buildsystem().meson().sourcedir = self.get_sourcedir()
        self._model.buildsystem().meson().builddir = self.get_builddir()
        self.meson_api.sourcedir = self.get_sourcedir()
        self.meson_api.builddir = self.get_builddir()

        SetupActivity(self.console, model=self._model)

    @pyqtSlot()
    def exec_conf(self) -> None:
        if not Path(join(self.get_builddir(), 'build.ninja')).exists() and \
           not Path(self.get_builddir()).is_dir():
            logging.warning('Block user from this action "builddir" directory not found')
            SnackBarMessage.warning(self, 'No builddir found',
                                          'There was no builddir found. Stop action.')
            return
        logging.info('Configure Meson build project with "meson configure" command')
        self._model.buildsystem().meson().sourcedir = self.get_sourcedir()
        self._model.buildsystem().meson().builddir = self.get_builddir()
        self.meson_api.sourcedir = self.get_sourcedir()
        self.meson_api.builddir = self.get_builddir()

        ConfigureActivity(self.console, model=self._model)
        self.dashboard.update(self.meson_api)

    @pyqtSlot()
    def exec_compile(self) -> None:
        if not Path(join(self.get_builddir(), 'build.ninja')).exists() and \
           not Path(self.get_builddir()).is_dir():
            logging.warning('Block user from this action "builddir" directory not found')
            SnackBarMessage.warning(self, 'No builddir found',
                                          'There was no builddir found. Stop action.')
            return
        logging.info('Compile build project')
        self.console.command_run(str(self._model.buildsystem().meson().compile()))
        self.dashboard.update(self.meson_api)

    @pyqtSlot()
    def exec_build(self) -> None:
        if not Path(join(self.get_builddir(), 'build.ninja')).exists() and \
           not Path(self.get_builddir()).is_dir():
            logging.warning('Block user from this action "builddir" directory not found')
            SnackBarMessage.warning(self, 'No builddir found',
                                          'There was no builddir found. Stop action.')
            return
        logging.info('Build project with "ninja" command')
        self.console.command_run(str(self._model.buildsystem().meson().build()))
        self.dashboard.update(self.meson_api)

    @pyqtSlot()
    def exec_introspect(self) -> None:
        logging.info('Getting project introspection data with "meson introspect" command')
        if Path(join(self.get_sourcedir(), 'meson.build')):
            self.dashboard.update(self.meson_api)

    @pyqtSlot()
    def exec_subprojects(self) -> None:
        if not Path(join(self.get_sourcedir(), 'subprojects')).exists():
            logging.warning('Block user from this action "subprojects" directory not found')
            SnackBarMessage.warning(self, 'No builddir found',
                                          'There was no subprojects directory found. Stop action.')
            return
        logging.info('Subproject manager with "meson subprojects" command')
        SubprojectsActivity(model=self._model)
        self.dashboard.update(self.meson_api)

    @pyqtSlot()
    def exec_wrap(self) -> None:
        if not Path(join(self.get_sourcedir(), 'subprojects')).exists():
            logging.warning(' Block user from this action "subprojects" directory not found')
            SnackBarMessage.warning(self, 'No builddir found',
                                          'There was no subprojects directory found. Stop action.')
            return
        logging.info(' WrapDB manager with "meson wrap" command')
        WrapActivity(model=self._model)
        self.dashboard.update(self.meson_api)

    @pyqtSlot()
    def exec_test(self) -> None:
        if Path(self.get_sourcedir()) == Path(self.get_builddir()):
            logging.warning(' Block user from this action, both "sourcedir" and "builddir" values is the same!')
            SnackBarMessage.warning(self, 'Sourcedir equale to Builddir',
                                          'Both entry values should not be the same.')
            return

        if not Path(join(self.get_builddir(), 'build.ninja')).exists() and \
           not Path(self.get_builddir()).is_dir():
            logging.warning(' Block user from this action "builddir" directory not found')
            SnackBarMessage.warning(self, 'No builddir found',
                                          'There was no builddir found. Stop action.')
            return
        logging.info('Run test cases written in the script')
        self.console.command_run(str(self._model.buildsystem().meson().test()))
        self.dashboard.update(self.meson_api)

    @pyqtSlot()
    def exec_clean(self) -> None:
        if Path(self.get_sourcedir()) == Path(self.get_builddir()):
            logging.warning(' Block user from this action, both "sourcedir" and "builddir" values is the same!')
            SnackBarMessage.warning(self, 'Sourcedir equale to Builddir',
                                          'Both entry values should not be the same.')
            return

        if not Path(join(self.get_builddir(), 'build.ninja')).exists() and \
           not Path(self.get_builddir()).is_dir():
            logging.warning(' Block user from this action "builddir" directory not found')
            SnackBarMessage.warning(self, 'No builddir found',
                                          'There was no builddir found. Stop action.')
            return
        logging.info('Cleanning project directory')
        self.console.command_run(str(self._model.buildsystem().meson().clean()))

    @pyqtSlot()
    def exec_install(self) -> None:
        if Path(self.get_sourcedir()) == Path(self.get_builddir()):
            logging.warning(' Block user from this action, both "sourcedir" and "builddir" values is the same!')
            SnackBarMessage.warning(self, 'Sourcedir equale to Builddir',
                                          'Both entry values should not be the same.')
            return

        if not Path(join(self.get_builddir(), 'build.ninja')).exists() and \
           not Path(self.get_builddir()).is_dir():
            logging.warning(' Block user from this action "builddir" directory not found')
            SnackBarMessage.warning(self, 'No builddir found',
                                          'There was no builddir found. Stop action.')
            return
        logging.info(' Install project with "meson install" command')
        InstallActivity(model=self._model)

    @pyqtSlot()
    def exec_init(self) -> None:
        self._model.buildsystem().meson().sourcedir = self.get_sourcedir()
        self._model.buildsystem().meson().builddir = self.get_builddir()
        logging.info(' Init new project template with "meson init" command')
        InitActivity(model=self._model)
        self.dashboard.update(self.meson_api)

    @pyqtSlot()
    def exec_dist(self) -> None:
        if Path(self.get_sourcedir()) == Path(self.get_builddir()):
            SnackBarMessage.warning(self, 'Sourcedir equale to Builddir',
                                          'Both entry values should not be the same.')
            return

        if not Path(join(self.get_builddir(), 'build.ninja')).exists() and \
           not Path(self.get_builddir()).is_dir():
            SnackBarMessage.warning(self, 'No builddir found',
                                          'There was no builddir found. Stop action.')
            return
        logging.info(' Create project with "meson dist" command')
        self._model.buildsystem().meson().sourcedir = self.get_sourcedir()
        self._model.buildsystem().meson().builddir = self.get_builddir()
        DistActivity(model=self._model)

    @pyqtSlot()
    def exec_open(self) -> None:
        source_root = str(QFileDialog.getExistingDirectory(self, 'Open Sourcedir', QDir.homePath()))
        if source_root != '':
            self._model.buildsystem().meson().sourcedir = source_root
            self._model.buildsystem().meson().builddir = join(source_root, 'builddir')
            self._model.buildsystem().ninja().sourcedir = source_root
            self._model.buildsystem().ninja().builddir = join(source_root, 'builddir')
            self.meson_api.sourcedir = source_root
            self.meson_api.builddir = join(source_root, 'builddir')
            self.project_sourcedir.setText(str(self._model.buildsystem().meson().sourcedir))
            self.project_builddir.setText(str(self._model.buildsystem().meson().builddir))
        else:
            logging.info(' User just closed file dialog.')
            return
        self.dashboard.update(self.meson_api)

    @pyqtSlot()
    def get_sourcedir(self) -> T.AnyStr:
        return self.project_sourcedir.text()

    @pyqtSlot()
    def get_builddir(self) -> T.AnyStr:
        return self.project_builddir.text()

    @pyqtSlot()
    def onclick_docs(self):
        self.on_open_url(url_link='https://mesonbuild.com')
    # end of method

    @pyqtSlot()
    def onclick_faqs(self):
        self.on_open_url(url_link='https://mesonbuild.com/FAQ.html')
    # end of method

    @pyqtSlot()
    def onclick_mesonui_issue(self):
        self.on_open_url(url_link='https://github.com/michaelbadcrumble/meson-ui/issues')
    # end of method

    @pyqtSlot()
    def onclick_meson_issue(self):
        self.on_open_url(url_link='https://github.com/mesonbuild/meson/issues')
    # end of method

    @pyqtSlot()
    def on_open_url(self, url_link: str = ''):
        url = QUrl(url_link)
        QDesktopServices.openUrl(url=url)
