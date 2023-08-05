#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
class ProjectAuthor:
    def __init__(self):
        self.info = {
            'name': 'Michael Brockus',
            'mail': 'michaelbrockus@gmail.com'
        }

    def get_name(self) -> str:
        return self.info['name']

    def get_mail(self) -> str:
        return self.info['mail']
