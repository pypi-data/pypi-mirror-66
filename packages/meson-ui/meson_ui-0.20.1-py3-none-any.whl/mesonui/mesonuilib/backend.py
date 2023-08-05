#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from .backends.codeblocks import CodeBlocksBackend
from .backends.qtcreator import QtCreatorBackend
from .backends.kdevelop import KDevelopBackend
from .backends.gnome import GNOMEBuilderBackend

from ..repository.mesonapi import MesonAPI
import logging


def backend_factory(backend: str, meson_api: MesonAPI):
    logging.info(f'User backend project for {backend}')
    return {
        'kdevelop': KDevelopBackend,
        'codeblocks': CodeBlocksBackend,
        'qtcreator': QtCreatorBackend,
        'gnome': GNOMEBuilderBackend
    }[backend](meson_api)
