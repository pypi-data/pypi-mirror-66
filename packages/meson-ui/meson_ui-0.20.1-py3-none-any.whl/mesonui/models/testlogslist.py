#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from ..containers.doublylist import MesonUiDLL


class TestsLogsModel:
    def __init__(self):
        super().__init__()
        self._dll: MesonUiDLL = MesonUiDLL()

    def get_list(self) -> MesonUiDLL:
        return self._dll

    def set_list(self, value) -> None:
        options = value.get_object(group='tests')
        testlog = value.get_object(group='testlog')
        if options is None or testlog is None:
            return

        while self._dll.head is not None:
            self._dll.remove_item()

        for values in range(len(options["tests"])):
            self._dll.append_item(f' suite:  {options["tests"][values]["suite"]}\n'
                                  f' name:   {options["tests"][values]["name"]}\n'
                                  f' result: {testlog["result"]}\n'
                                  '---------------------------------------------------------------------------------------------------:')
