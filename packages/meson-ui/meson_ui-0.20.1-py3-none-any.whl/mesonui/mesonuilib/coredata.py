#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from .appconfig.core import MesonCoreConfig
from .appconfig.base import MesonBaseConfig
from .appconfig.test import MesonTestConfig
from .appconfig.path import MesonPathConfig
from .appconfig.dist import MesonDistConfig
from .appconfig.init import MesonInitConfig
from .appconfig.install import MesonInstallConfig
from .appconfig.backend import MesonBackendConfig

from .mapmeson import default_backend
from .mapmeson import default_core
from .mapmeson import default_base
from .mapmeson import default_path
from .mapmeson import default_test
from .mapmeson import default_dist
from .mapmeson import default_init
from .mapmeson import default_install

import typing as T


class MesonUiCache:
    def __init__(self):
        self._conf_core: MesonCoreConfig = MesonCoreConfig()
        self._conf_base: MesonBaseConfig = MesonBaseConfig()
        self._conf_test: MesonTestConfig = MesonTestConfig()
        self._conf_path: MesonPathConfig = MesonPathConfig()
        self._conf_backend: MesonBackendConfig = MesonBackendConfig()

    def init_cache(self):
        self._init_cache_core()
        self._init_cache_base()
        self._init_cache_test()
        self._init_cache_path()
        self._init_cache_backend()

    def _init_cache_core(self) -> None:
        for conf in default_core:
            self._conf_core.config(conf, default_core[conf][0])

    def _init_cache_base(self) -> None:
        for conf in default_base:
            self._conf_base.config(conf, default_base[conf][0])

    def _init_cache_test(self) -> None:
        for conf in default_test:
            self._conf_test.config(conf, default_test[conf][0])

    def _init_cache_path(self) -> None:
        for conf in default_path:
            self._conf_path.config(conf, default_path[conf][0])

    def _init_cache_backend(self) -> None:
        for conf in default_backend:
            self._conf_backend.config(conf, default_backend[conf][0])

    def configure_core(self, option: T.AnyStr, value: T.AnyStr = ''):
        self._conf_core.config(option=option, value=value)

    def configure_base(self, option: T.AnyStr, value: T.AnyStr = ''):
        self._conf_base.config(option=option, value=value)

    def configure_test(self, option: T.AnyStr, value: T.AnyStr = ''):
        self._conf_test.config(option=option, value=value)

    def configure_path(self, option: T.AnyStr, value: T.AnyStr = ''):
        self._conf_path.config(option=option, value=value)

    def configure_backend(self, option: T.AnyStr, value: T.AnyStr = ''):
        self._conf_backend.config(option=option, value=value)

    def get_core(self) -> T.Dict[T.AnyStr, set]:
        return self._conf_core.extract()

    def get_base(self) -> T.Dict[T.AnyStr, set]:
        return self._conf_base.extract()

    def get_test(self) -> T.Dict[T.AnyStr, set]:
        return self._conf_test.extract()

    def get_path(self) -> T.Dict[T.AnyStr, set]:
        return self._conf_path.extract()

    def get_backend(self) -> T.Dict[T.AnyStr, set]:
        return self._conf_backend.extract()


class MesonUiDistCache:
    def __init__(self):
        self._conf_dist: MesonDistConfig = MesonDistConfig()

    def init_cache(self) -> None:
        for conf in default_dist:
            self._conf_dist.config(conf, default_dist[conf][0])

    def configure(self, option: T.AnyStr, value: T.AnyStr = ''):
        self._conf_dist.config(option=option, value=value)

    def get_cache(self) -> T.Dict[T.AnyStr, set]:
        return self._conf_dist.extract()


class MesonUiInitCache:
    def __init__(self):
        self._conf_init: MesonInitConfig = MesonInitConfig()

    def init_cache(self) -> None:
        for conf in default_init:
            self._conf_init.config(conf, default_init[conf][0])

    def configure(self, option: T.AnyStr, value: T.AnyStr = ''):
        self._conf_init.config(option=option, value=value)

    def get_cache(self) -> T.Dict[T.AnyStr, set]:
        return self._conf_init.extract()


class MesonUiInstallCache:
    def __init__(self):
        self._conf_install: MesonInstallConfig = MesonInstallConfig()

    def init_cache(self) -> None:
        for conf in default_install:
            self._conf_install.config(conf, default_install[conf][0])

    def configure(self, option: T.AnyStr, value: T.AnyStr = ''):
        self._conf_install.config(option=option, value=value)

    def get_cache(self) -> T.Dict[T.AnyStr, set]:
        return self._conf_install.extract()
