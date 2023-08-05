# -*- coding: utf-8 -*-
"""sconstool.cxxtestgen

Tool-specific initialization for cxxtestgen.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""

#
# Copyright (c) 2018-2020 by Paweł Tomulik
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from .about import __version__
from .detail_ import *

import SCons.Builder
import SCons.Action
import SCons.Util
import SCons.Tool
import sys
import os

cxxTestGenCom = '$CXXTESTGENPYTHON $CXXTESTGEN $_CXXTESTGENFLAGS -o $TARGET $SOURCES'
cxxTestGenRootCom = '$CXXTESTGENPYTHON $CXXTESTGEN --root $_CXXTESTGENFLAGS -o $TARGET'
cxxTestGenPartCom = '$CXXTESTGENPYTHON $CXXTESTGEN --part $_CXXTESTGENFLAGS -o $TARGET $SOURCES'
cxxTestGenAction = SCons.Action.Action('$CXXTESTGENCOM', '$CXXTESTGENCOMSTR')
cxxTestGenRootAction = SCons.Action.Action('$CXXTESTGENROOTCOM', '$CXXTESTGENROOTCOMSTR')
cxxTestGenPartAction = SCons.Action.Action('$CXXTESTGENPARTCOM', '$CXXTESTGENPARTCOMSTR')

def createCxxTestGenBuilder(env):
    try:
        builder = env['BUILDERS']['CxxTestGen']
    except KeyError:
        builder = SCons.Builder.Builder(action=cxxTestGenAction,
                                        emitter={},
                                        suffix={None: '$CXXTESTGENSUFFIX'},
                                        src_suffix=['$CXXTESTGENSRCSUFFIX'])
        env['BUILDERS']['CxxTestGen'] = builder
    return builder

def createCxxTestGenRootBuilder(env):
    try:
        builder = env['BUILDERS']['_CxxTestGenRoot']
    except KeyError:
        builder = SCons.Builder.Builder(action=cxxTestGenRootAction,
                                        emitter={},
                                        suffix={None: '$CXXTESTGENSUFFIX'})
        env['BUILDERS']['_CxxTestGenRoot'] = builder
    try:
        env.CxxTestGenRoot
    except AttributeError:
        env.AddMethod(_CxxTestGenRootWrapper, 'CxxTestGenRoot')
    return builder

def createCxxTestGenPartBuilder(env):
    try:
        builder = env['BUILDERS']['CxxTestGenPart']
    except KeyError:
        builder = SCons.Builder.Builder(action=cxxTestGenPartAction,
                                        emitter={},
                                        suffix={None: '$CXXTESTGENSUFFIX'},
                                        src_suffix=['$CXXTESTGENSRCSUFFIX'])
        env['BUILDERS']['CxxTestGenPart'] = builder
    return builder

def _CxxTestGenRootWrapper(env, target, **kw):
    return env._CxxTestGenRoot(target, [], **kw)


def setCxxTestGenDefaults(env):
    cxxtestgen = findCxxTestGen(env)
    python = findCxxTestGenPython(env, cxxtestgen)

    env.SetDefault(CXXTESTGENPYTHON=python or sys.executable)
    env.SetDefault(CXXTESTGEN=cxxtestgen or 'cxxtestgen')
    env.SetDefault(CXXTESTGENRUNNER='ErrorPrinter')
    env.SetDefault(CXXTESTGENFLAGS=SCons.Util.CLVar())
    env.SetDefault(CXXTESTGENSUFFIX='.t.cpp')
    env.SetDefault(CXXTESTGENSRCSUFFIX='.t.h')
    env.SetDefault(CXXTESTGENCOM=cxxTestGenCom, CXXTESTGENCOMSTR='$CXXTESTGENCOM')
    env.SetDefault(CXXTESTGENROOTCOM=cxxTestGenRootCom, CXXTESTGENROOTCOMSTR='$CXXTESTGENROOTCOM')
    env.SetDefault(CXXTESTGENPARTCOM=cxxTestGenPartCom, CXXTESTGENPARTCOMSTR='$CXXTESTGENPARTCOM')
    env['_CXXTESTGENRUNNER'] = '${_concat("--runner=",CXXTESTGENRUNNER,"",__env__)}'
    env['_CXXTESTGENFLAGS'] = SCons.Util.CLVar(['$_CXXTESTGENRUNNER', '$CXXTESTGENFLAGS'])



def extendCXXFileBuilder(env):
    _, cxx = SCons.Tool.createCFileBuilders(env)
    cxx.add_action('.t.h', '$CXXTESTGENCOM')
    cxx.set_suffix(Selector(cxx.suffix))
    cxx.suffix['$CXXTESTGENSRCSUFFIX'] = '$CXXTESTGENSUFFIX'


def generate(env):
    createCxxTestGenBuilder(env)
    createCxxTestGenRootBuilder(env)
    createCxxTestGenPartBuilder(env)
    extendCXXFileBuilder(env)
    setCxxTestGenDefaults(env)


def exists(env):
    return env.Detect(env.get('CXXTESTGEN', findCxxTestGen(env) or 'cxxtestgen'))

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
