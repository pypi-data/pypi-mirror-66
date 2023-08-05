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


class MesonInit:
    def __init__(self, sourcedir: Path):
        super().__init__()
        self._sourcedir: Path = sourcedir

    def run(self, args: list = []):
        run_cmd = ['meson', 'init', '-C', str(self._sourcedir)]
        run_cmd.extend(args)
        process = subprocess.Popen(run_cmd, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.communicate()[0]
