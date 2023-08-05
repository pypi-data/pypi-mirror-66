#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
import subprocess


class MesonWrap:
    def __init__(self):
        super().__init__()

    def update(self, wrap_args) -> None:
        run_cmd = ['meson', 'wrap', 'update', wrap_args]
        process = subprocess.Popen(run_cmd, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.communicate()[0]

    def search(self, wrap_args) -> None:
        run_cmd = ['meson', 'wrap', 'search', wrap_args]
        process = subprocess.Popen(run_cmd, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.communicate()[0]

    def info(self, wrap_args) -> None:
        run_cmd = ['meson', 'wrap', 'info', wrap_args]
        process = subprocess.Popen(run_cmd, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.communicate()[0]

    def install(self, wrap_args) -> None:
        run_cmd = ['meson', 'wrap', 'install', wrap_args]
        process = subprocess.Popen(run_cmd, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.communicate()[0]

    def list_wraps(self) -> None:
        run_cmd = ['meson', 'wrap', 'list']
        process = subprocess.Popen(run_cmd, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.communicate()[0]

    def status(self) -> None:
        run_cmd = ['meson', 'wrap', 'status']
        process = subprocess.Popen(run_cmd, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.communicate()[0]
