#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from pathlib import Path
import subprocess


class MesonConfigure:
    def __init__(self, builddir: Path):
        self._builddir: Path = builddir
        super().__init__()

    def run(self, args: list = []):
        run_cmd = ['meson', 'configure', str(self._builddir)]
        run_cmd.extend(args)
        process = subprocess.Popen(run_cmd, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.communicate()[0]
