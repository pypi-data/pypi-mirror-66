#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
# here we use a lot of data models
from .projectinfolist import ProjectInfoModel
from .buildoptions import BuildOptionsModel
from .testlogslist import TestsLogsModel
from .buildsystem import BuildSystemModel
from .configure import ConfigureModel


class MainModel:
    def __init__(self):
        self._configure: ConfigureModel = ConfigureModel()
        self._buildoptions: BuildOptionsModel = BuildOptionsModel()
        self._testlogs: TestsLogsModel = TestsLogsModel()
        self._projectinfo: ProjectInfoModel = ProjectInfoModel()
        self._build_sys: BuildSystemModel = BuildSystemModel()

    def model_options(self) -> BuildOptionsModel:
        return self._buildoptions

    def model_testlogsinfo(self) -> TestsLogsModel:
        return self._testlogs

    def buildsysteminfo(self) -> ProjectInfoModel:
        return self._projectinfo

    def model_configure(self) -> ConfigureModel:
        return self._configure

    def buildsystem(self) -> BuildSystemModel:
        return self._build_sys
