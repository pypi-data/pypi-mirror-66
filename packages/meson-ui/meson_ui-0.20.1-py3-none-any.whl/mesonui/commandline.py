#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from .projectinfo import ProjectInfo
import argparse


def mesonui_cli() -> argparse:
    data: ProjectInfo = ProjectInfo()

    parser: argparse = argparse.ArgumentParser(description='Meson-ui Build GUI.')

    parser.add_argument('-v', '--version', action='version', version=data.get_version(), help='print version number')

    parser.parse_args()
