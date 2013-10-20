# -*- coding: utf-8 -*-

# Copyright 2013 Jacek Mitręga

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals


_unspecified = object()


class ObjectProxy(object):

    __slots__ = ('__target__',)

    def __init__(self, target=_unspecified):
        if not target is _unspecified:
            self.__target__ = target

    def __getattribute__(self, attr):
        target = object.__getattribute__(self, '__target__')
        return target if attr == '__target__' else getattr(target, attr)

    def __setattr__(self, attr, value):
        if attr == '__target__':
            object.__setattr__(self, attr, value)
        else:
            setattr(self.__target__, attr, value)

    def __delattr__(self, attr):
        if attr == '__target__':
            object.__delattr__(self, attr)
        else:
            delattr(self.__target__, attr)
