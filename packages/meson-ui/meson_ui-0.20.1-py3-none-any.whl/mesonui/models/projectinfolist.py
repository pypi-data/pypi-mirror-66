#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from ..containers.doublylist import MesonUiDLL


class ProjectInfoModel:
    def __init__(self):
        super().__init__()
        self._dll: MesonUiDLL = MesonUiDLL()

    def get_list(self) -> MesonUiDLL:
        return self._dll

    def set_list(self, value) -> None:
        options = value.get_object(group='projectinfo')
        if options is None:
            return

        while self._dll.head is not None:
            self._dll.remove_item()

        self._dll.append_item(f' descriptive_name: {options["descriptive_name"]}\n'
                              f' target version:   {options["version"]}\n'
                              f' subproject_dir:   {options["subproject_dir"]}\n'
                              f' subprojects: {len(options["subprojects"])}\n'
                              '---------------------------------------------------------------------------------------------------:')

        for values in range(len(options['subprojects'])):
            self._dll.append_item(f' Subproject:\n'
                                  f' descriptive_name:  {options["subprojects"][values]["descriptive_name"]:<65}\n'
                                  f' target version:    {options["subprojects"][values]["version"]:<65}\n'
                                  f' target name:       {options["subprojects"][values]["name"]:<10}\n'
                                  '---------------------------------------------------------------------------------------------------:')
