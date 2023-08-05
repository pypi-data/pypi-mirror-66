#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#


class ConfigureModel:
    def __init__(self):
        super().__init__()
        self._configure: list = []

    def get_configure(self) -> list:
        return self._configure

    def set_configure(self, value: list) -> None:
        self._scriptdir = value
