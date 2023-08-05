#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from mesonui.mesonuilib.utilitylib import MesonUiException


MESON_OPTION_TYPES = {
    'string',
    'boolean',
    'combo',
    'integer',
    'array'
}

MESON_OPTION_SECTION = {
    'core',
    'backend',
    'base',
    'compiler',
    'directory',
    'user',
    'test',
}

MESON_OPTION_MACHINE = {
    'any',
    'host',
    'build'
}


class ComboBuildOption:
    def __init__(self, info: any):
        self.type = 'combo'
        self.name = info['name']
        self.value = info['value']
        self.section = info['section']
        self.machine = info['machine']
        self.description = info['description']
        self.choices = info['choices']


class ArrayBuildOption:
    def __init__(self, info: any):
        self.type = 'array'
        self.name = info['name']
        self.value = info['value']
        self.section = info['section']
        self.machine = info['machine']
        self.description = info['description']


class StringBuildOption:
    def __init__(self, info: any):
        self.type = 'string'
        self.name = info['name']
        self.value = info['value']
        self.section = info['section']
        self.machine = info['machine']
        self.description = info['description']


class BooleanBuildOption:
    def __init__(self, info: any):
        self.type = 'boolean'
        self.name = info['name']
        self.value = info['value']
        self.section = info['section']
        self.machine = info['machine']
        self.description = info['description']


class IntegerBuildOption:
    def __init__(self, info: any):
        self.type = 'integer'
        self.name = info['name']
        self.value = info['value']
        self.section = info['section']
        self.machine = info['machine']
        self.description = info['description']


class BuildOption:
    def __init__(self, meson_api):
        self.options = meson_api.get_object(group='buildoptions', extract_method='loader')

    def _find_option(self, name):
        for option in self.options:
            if option['name'] == name:
                if not option['machine'] in MESON_OPTION_MACHINE:
                    raise MesonUiException()

                if not option['section'] in MESON_OPTION_SECTION:
                    raise MesonUiException()

                if not option['type'] in MESON_OPTION_TYPES:
                    raise MesonUiException()
                return option
        raise MesonUiException(f'Option {name} not found!')

    def combo(self, name: str) -> ComboBuildOption:
        if not isinstance(name, str):
            raise MesonUiException(f'Option has wrong type {type(name)} should be string!')
        opt = self._find_option(name)
        if opt['type'] != 'combo':
            raise MesonUiException('Option has wrong type!')
        return ComboBuildOption(opt)

    def array(self, name: str) -> ArrayBuildOption:
        if not isinstance(name, str):
            raise MesonUiException(f'Option has wrong type {type(name)} should be string!')
        opt = self._find_option(name)
        if opt['type'] != 'array':
            raise MesonUiException('Option has wrong type!')
        return ArrayBuildOption(opt)

    def string(self, name: str) -> StringBuildOption:
        if not isinstance(name, str):
            raise MesonUiException(f'Option has wrong type {type(name)} should be string!')
        opt = self._find_option(name)
        if opt['type'] != 'string':
            raise MesonUiException('Option has wrong type!')
        return StringBuildOption(opt)

    def integer(self, name: str) -> IntegerBuildOption:
        if not isinstance(name, str):
            raise MesonUiException(f'Option has wrong type {type(name)} should be string!')
        opt = self._find_option(name)
        if opt['type'] != 'integer':
            raise MesonUiException('Option has wrong type!')
        return IntegerBuildOption(opt)

    def boolean(self, name: str) -> BooleanBuildOption:
        if not isinstance(name, str):
            raise MesonUiException(f'Option has wrong type {type(name)} should be string!')
        opt = self._find_option(name)
        if opt['type'] != 'boolean':
            raise MesonUiException('Option has wrong type!')
        return BooleanBuildOption(opt)
