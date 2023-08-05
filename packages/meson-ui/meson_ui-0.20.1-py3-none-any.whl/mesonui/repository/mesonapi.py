#!/usr/bin/env python3
#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from ..mesonuilib.utilitylib import MesonUiException
from .datascanner import MesonScriptReader
from .datareader import MesonBuilddirReader
from .dataloader import MesonBuilddirLoader
from .dataloader import _MESON_INTRO_FILES
from pathlib import Path
from os.path import join as join_paths
import logging


class MesonAPI:
    def __init__(self, sourcedir: Path = Path().cwd(), builddir: Path = join_paths(Path().cwd(), 'builddir')):
        super().__init__()
        self._sourcedir: Path = sourcedir
        self._builddir: Path = builddir

    @property
    def sourcedir(self):
        return self._sourcedir

    @property
    def builddir(self):
        return self._builddir

    @sourcedir.setter
    def sourcedir(self, new_dir: Path):
        self._sourcedir = new_dir

    @builddir.setter
    def builddir(self, new_dir: Path):
        self._builddir = new_dir

    def get_object(self, group: str = None, extract_method: str = 'script', use_fallback: bool = False) -> any:
        if not isinstance(group, str):
            raise MesonUiException(f'API group key pair {type(group)} is not valid type!')

        if not isinstance(extract_method, str):
            raise MesonUiException(f'API extract method {type(extract_method)} is not valid type!')

        logging.info(f'protocol settings: use_fallback={use_fallback}, group={group}, extract={extract_method}')
        if extract_method == 'reader':
            if use_fallback is False and self._has_intro_files() and self._is_builddir():
                return MesonBuilddirReader(self.builddir).extract_from(group=group)
            elif use_fallback is True or self._has_meson_script() and self._is_sourcedir():
                return MesonScriptReader(self.sourcedir).extract_from(group=group)
            else:
                return None

        elif extract_method == 'loader':
            if use_fallback is False and self._has_intro_files() and self._is_builddir():
                return MesonBuilddirLoader(self.builddir).extract_from(group=group)
            elif use_fallback is True or self._has_meson_script() and self._is_sourcedir():
                return MesonScriptReader(self.sourcedir).extract_from(group=group)
            else:
                return None

        elif extract_method == 'script':
            if use_fallback is True or self._has_meson_script() and self._is_sourcedir():
                return MesonScriptReader(self.sourcedir).extract_from(group=group)
            else:
                return None
        else:
            raise MesonUiException(f'Extract method {extract_method} not found in Meson "JSON" API!')

    def _is_builddir(self):
        return True if Path(self._builddir).exists() and \
            Path(self._builddir).is_dir() else False

    def _is_sourcedir(self):
        return True if Path(self._sourcedir).exists() and \
            Path(self._sourcedir).is_dir() else False

    def _has_meson_script(self):
        return True if Path(join_paths(self._sourcedir, 'meson.build')).exists() else False

    def _has_intro_files(self):
        for file in range(len(_MESON_INTRO_FILES)):
            if not Path(join_paths(self._builddir, 'meson-info', _MESON_INTRO_FILES[file])).exists():
                return False
        return True
