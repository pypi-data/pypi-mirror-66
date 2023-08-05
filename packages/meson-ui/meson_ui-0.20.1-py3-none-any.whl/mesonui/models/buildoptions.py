#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from ..containers.doublylist import MesonUiDLL


class BuildOptionsModel:
    def __init__(self):
        super().__init__()
        self._dll: MesonUiDLL = MesonUiDLL()

    def get_list(self) -> MesonUiDLL:
        return self._dll

    def set_list(self, value) -> None:
        options = value.get_object(group='buildoptions')
        if options is None:
            return

        while self._dll.head is not None:
            self._dll.remove_item()

        for values in range(len(options)):
            self._dll.append_item(f' section: {options[values]["section"]}\n'
                                  f' option:  {options[values]["name"]:<25}\n'
                                  f' value:   {str(options[values]["value"]):<65}\n'
                                  f' type:    {str(options[values]["type"]):<65}\n'
                                  f' description: {options[values]["description"]:<10}\n'
                                  '---------------------------------------------------------------------------------------------------:')
