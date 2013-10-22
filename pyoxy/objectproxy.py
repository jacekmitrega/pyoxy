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


try:  # pragma: no cover
    unicode
    PY3 = False
except NameError:  # pragma: no cover
    PY3 = True


_unspecified = object()


def _proxy_fn(fn):
    return lambda self: fn(self.__target__)


class ObjectProxy(object):

    __slots__ = ('__target__', '__weakref__')

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

    def __dir__(self):
        return dir(self.__target__) + list((ObjectProxy.__slots__))

    def __get__(self, instance, owner):
        return self.__target__.__get__(instance, owner)

    def __set__(self, instance, value):
        return self.__target__.__set__(instance, value)

    def __delete__(self, instance):
        return self.__target__.__delete__(instance)

    __repr__ = _proxy_fn(repr)
    __str__ = _proxy_fn(str)
    if PY3:  # pragma: no cover
        __bytes__ = _proxy_fn(bytes)
    else:  # pragma: no cover
        __unicode__ = _proxy_fn(unicode)

    def __format__(self, format_spec):
        return format(self.__target__, format_spec)

    def __lt__(self, other):
        return self.__target__ < other

    def __le__(self, other):
        return self.__target__ <= other

    def __eq__(self, other):
        return self.__target__ == other

    def __ne__(self, other):
        return self.__target__ != other

    def __gt__(self, other):
        return self.__target__ > other

    def __ge__(self, other):
        return self.__target__ >= other

    if not PY3:  # pragma: no cover
        def __cmp__(self, other):
            if isinstance(other, ObjectProxy):
                other = other.__target__
            return cmp(self.__target__, other)

    __hash__ = _proxy_fn(hash)

    __bool__ = _proxy_fn(bool)
    if not PY3:  # pragma: no cover
        __nonzero__ = __bool__
        del __bool__

    def __instancecheck__(self, instance):
        """
        Handle 'isinstance(object, ObjectProxy(classinfo))'.

        """
        return isinstance(instance, self.__target__)

    def __subclasscheck__(self, subclass):
        """
        Handle 'issubclass(class, ObjectProxy(classinfo))'.

        """
        if isinstance(subclass, ObjectProxy):
            subclass = subclass.__target__
        return issubclass(subclass, self.__target__)

    def __call__(self, *args, **kwargs):
        return self.__target__(*args, **kwargs)
