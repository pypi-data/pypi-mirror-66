#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from .mesonbuild.subprojects import MesonSubprojects
from .mesonbuild.configure import MesonConfigure
from .mesonbuild.install import MesonInstall
from .mesonbuild.version import MesonVersion
from .mesonbuild.compile import MesonCompile
from .mesonbuild.setup import MesonSetup
from .mesonbuild.clean import MesonClean
from .mesonbuild.init import MesonInit
from .mesonbuild.dist import MesonDist
from .mesonbuild.wrap import MesonWrap
from .mesonbuild.test import MesonTest

from .ninjabuild.install import NinjaInstall
from .ninjabuild.version import NinjaVersion
from .ninjabuild.build import NinjaBuild
from .ninjabuild.clean import NinjaClean
from .ninjabuild.dist import NinjaDist
from .ninjabuild.test import NinjaTest

from .utilitylib import find_executables
from os.path import join as join_paths
from pathlib import Path
import logging


class Meson:
    '''
    this class is a wrapper for the Meson build system.
    '''
    def __init__(self, sourcedir: Path = Path().cwd(), builddir: Path = join_paths(Path().cwd(), 'builddir')):
        super().__init__()
        self.name = 'Meson build'
        self.exe = find_executables(['meson', 'meson.py'])
        self._sourcedir = sourcedir
        self._builddir = builddir
    # end of method

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

    def version(self) -> MesonVersion:
        logging.info(f'Getting {self.name} version')
        return MesonVersion().run()

    def configure(self, args: list = []) -> MesonConfigure:
        logging.info(f'Configure {self.name} project')
        return MesonConfigure(self.builddir).run(args=args)

    def setup(self, args: list = []) -> MesonSetup:
        logging.info(f'Setting up new {self.name} project')
        return MesonSetup(self.sourcedir, self.builddir).run(args=args)

    def subprojects(self) -> MesonSubprojects:
        logging.info(f'Getting {self.name} subproject commands')
        return MesonSubprojects(self.sourcedir)

    def compile(self, args: list = []) -> MesonCompile:
        logging.info(f'Compile {self.name} project')
        return MesonCompile(self.builddir).run(args=args)

    def install(self, args: list = []) -> MesonInstall:
        logging.info(f'Install {self.name} project')
        return MesonInstall(self.builddir).run(args=args)

    def build(self) -> NinjaBuild:
        logging.info(f'Build {self.name} project')
        return NinjaBuild(self.builddir).run()

    def clean(self) -> MesonClean:
        logging.info(f'Clean {self.name} project')
        return MesonClean(self.builddir).run()

    def init(self, args: list = []) -> MesonInit:
        logging.info(f'Create new {self.name} project with: {args}')
        return MesonInit(self.sourcedir).run(args=args)

    def dist(self, args: list = []) -> MesonDist:
        logging.info(f'Create a {self.name} release with: {args}')
        return MesonDist(self.builddir).run(args=args)

    def test(self) -> MesonTest:
        logging.info(f'Test {self.name} project')
        return MesonTest(self.builddir).run()

    def wrap(self) -> MesonWrap:
        logging.info(f'Getting {self.name} wrap-tools commands')
        return MesonWrap()


class Ninja:
    '''
    this class is a wrapper for the Ninja build system.
    '''
    def __init__(self, sourcedir: Path = Path().cwd(), builddir: Path = join_paths(Path().cwd(), 'builddir')):
        self.name = 'Ninja-build'
        self.exe = find_executables(['ninja-build', 'ninja'])
        self._sourcedir = sourcedir
        self._builddir = builddir

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

    def version(self) -> NinjaVersion:
        logging.info(f'Getting {self.name} version')
        return NinjaVersion().run()

    def install(self, args: list = []) -> NinjaInstall:
        logging.info(f'Install {self.name} project')
        return NinjaInstall(self.builddir).run(args=args)

    def build(self) -> NinjaBuild:
        logging.info(f'Build {self.name} project')
        return NinjaBuild(self.builddir).run()

    def clean(self) -> NinjaClean:
        logging.info(f'Clean {self.name} project')
        return NinjaClean(self.builddir).run()

    def dist(self, args: list = []) -> NinjaDist:
        logging.info(f'Dist new release with {self.name} project')
        return NinjaDist(self.builddir).run(args=args)

    def test(self) -> NinjaTest:
        logging.info(f'Tests {self.name} project')
        return NinjaTest(self.builddir).run()
