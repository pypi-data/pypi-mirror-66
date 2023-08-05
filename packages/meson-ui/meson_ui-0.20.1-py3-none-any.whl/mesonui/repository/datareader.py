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
import logging
import json


class MesonBuilddirReader:
    def __init__(self, builddir: Path = None):
        self._builddir: Path = builddir

    def _introspect(self, args: list) -> any:
        cmd: list = ['meson', 'introspect']
        cmd.extend(args)
        proc = subprocess.Popen(cmd, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc.communicate()[0]

    def _scan(self, group: str) -> any:
        info: any = json.loads(self._introspect([group, '--force-object-output', str(self._builddir)]))
        return info

    def extract_from(self, group: str) -> any:
        #
        # We need to make sure to return None if testlogs.json is not found. So
        # check to see if the group is "testlog" and if so give nothing back
        logging.info(f'Try getting {group} API object via read build directory.')
        if group == 'testlog':
            return None
        elif group == 'buildoptions':
            info = self._scan(group=f'--{group}')
            return info[group]
        elif group == 'tests':
            info = self._scan(group=f'--{group}')
            return info[group]
        elif group == 'benchmarks':
            info = self._scan(group=f'--{group}')
            return info[group]
        elif group == 'buildsystem-files':
            info = self._scan(group=f'--{group}')
            return info['buildsystem_files']
        elif group == 'projectinfo':
            info = self._scan(group=f'--{group}')
            return info[group]
        elif group == 'scan-dependencies':
            info = self._scan(group=f'--{group}')
            return info
        elif group == 'dependencies':
            info = self._scan(group=f'--{group}')
            return info[group]
        elif group == 'installed':
            info = self._scan(group=f'--{group}')
            return info[group]
        elif group == 'targets':
            info = self._scan(group=f'--{group}')
            return info[group]
        else:
            raise Exception(f'Group tag {group} not found in extract via data options!')
