#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
class MesonUiStack:
    def __init__(self):
        self.stack: list = list()

    def push(self, data):
        if data not in self.stack:
            self.stack.append(data)
            return True
        else:
            return False

    def pop(self):
        if len(self.stack) <= 0:
            return None
        else:
            return self.stack.pop()
