#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from .utilitylib import default_libexecdir
from .utilitylib import default_prefix
from .utilitylib import default_libdir


default_core: map = {
    'auto-features':     ('auto', 'enabled', 'disabled'),
    'backend':           ('ninja', 'xcode', 'qtcreator', 'codeblocks', 'gnome',
                          'kdevelop', 'vs2010', 'vs2015', 'vs2017', 'vs2019'),
    'buildtype':         ('debug', 'plain', 'release', 'debugoptimized', 'minsize', 'custom'),
    'default-library':   ('shared', 'static', 'both'),
    'layout':            ('mirror', 'flat'),
    'warnlevel':         ('0', '1', '2', '3'),
    'wrap-mode':         ('default', 'nofallback', 'nodownload', 'forcefallback'),
    'unity':             ('off', 'on', 'subprojects'),
    'werror':            ('false', 'true'),
    'strip':             ('false', 'true'),
    'cmake-prefix-path': ('.'),
    'pkg-config-path':   ('.'),
    'fatal-meson-warnings': ('true', 'false')
}

default_test: map = {
    'stdsplit': ('true', 'false'),
    'errorlogs': ('true', 'false')
}

default_path: map = {
    'prefix':         (default_prefix()),
    'bindir':         ('bin'),
    'datadir':        ('share'),
    'includedir':     ('include'),
    'infodir':        ('share/info'),
    'libdir':         (default_libdir()),
    'libexecdir':     (default_libexecdir()),
    'localedir':      ('share/locale'),
    'localstatedir':  ('var'),
    'mandir':         ('share/man'),
    'sbindir':        ('sbin'),
    'sharedstatedir': ('com'),
    'sysconfdir':     ('etc'),
}

default_base: map = {
    'b_colorout':  ('always', 'auto', 'never'),
    'b_coverage':  ('false', 'true'),
    'b_lundef':    ('true', 'false'),
    'b_lto':       ('true', 'false'),
    'b_ndebug':    ('false', 'true', 'if-release'),
    'b_pch':       ('true', 'false'),
    'b_pgo':       ('off', 'generate', 'use'),
    'b_sanitize':  ('none', 'address', 'thread', 'undefined', 'memory', 'address,undefined'),
    'b_staticpic': ('true', 'false'),
    'b_pie':       ('false', 'true'),
    'b_vscrt':     ('none', 'md', 'mdd', 'mt', 'mtd', 'from_buildtype')
}

default_backend: map = {
    'backend_max_links': ('0')
}

#
#
default_dist: map = {
    'formats': ('xztar', 'gztar', 'zip'),
    'include-subprojects': ('false', 'true')
}

default_init: map = {
    'type': ('executable', 'library'),
    'name': ('demo'),
    'version': ('0.1'),
    'language': ('c', 'cpp', 'cs', 'cuda', 'd', 'fortran', 'java', 'rust', 'objc', 'objcpp'),
}

default_install: map = {
    'on-rebuild': ('false', 'true'),
    'only-changed': ('false', 'true'),
    'quiet': ('false', 'true')
}
