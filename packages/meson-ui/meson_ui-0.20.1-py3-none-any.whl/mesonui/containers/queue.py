#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#

class MesonUiQueue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, data):
        if data not in self.items:
            self.items.append(data)
        else:
            return None

    def dequeue(self):
        print(len(self.items))
        if len(self.items) == 0:
            return None
        else:
            return self.items.pop(0)
