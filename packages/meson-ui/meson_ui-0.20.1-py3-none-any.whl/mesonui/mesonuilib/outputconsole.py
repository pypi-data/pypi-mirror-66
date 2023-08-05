#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#

class OutputConsole:
    def __init__(self, context=None):
        self._context = context

    def append_line(self, text: str) -> None:
        if text == '':
            return
        cursor = self._context.output_console.textCursor()
        self._context.output_console.setTextCursor(cursor)
        cursor.setPosition(cursor.Start)
        cursor.movePosition(cursor.Left, cursor.KeepAnchor, 3)
        self._context.output_console.ensureCursorVisible()

    def command_run(self, text: str):
        self._context.output_console.setPlainText(text)
        self.append_line(text)
