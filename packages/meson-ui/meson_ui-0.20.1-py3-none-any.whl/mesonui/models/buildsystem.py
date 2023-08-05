#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from ..mesonuilib.buildsystem import Meson
from ..mesonuilib.buildsystem import Ninja


class BuildSystemModel:
    def __init__(self):
        super().__init__()
        self._meson: Meson = Meson()
        self._ninja: Ninja = Ninja()

    def meson(self) -> Meson:
        return self._meson

    def ninja(self) -> Ninja:
        return self._ninja
