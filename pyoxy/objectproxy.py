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

from __future__ import division, unicode_literals

import operator


try:  # pragma: no cover
    unicode
    _PY3 = False
except NameError:  # pragma: no cover
    _PY3 = True


_unspecified = object()


def _proxy_fn(fn):
    return lambda self: fn(self.__target__)


UNARY_OP_METHOD_TEMPLATE = """
def __{method}__(self):
    return {op}self.__target__
"""
BINARY_OP_METHOD_TEMPLATE = """
def __{method}__(self, other):
    return self.__target__ {op} other
"""
BINARY_R_OP_METHOD_TEMPLATE = """
def __r{method}__(self, other):
    return other {op} self.__target__
"""
BINARY_I_OP_METHOD_TEMPLATE = """
def __i{method}__(self, other):
    self.__target__ {op}= other
    return self
"""


def _proxy_unary_op(method, op):
    return UNARY_OP_METHOD_TEMPLATE.format(method=method, op=op)


def _proxy_binary_op(method, op, r=False, i=False):
    template = BINARY_OP_METHOD_TEMPLATE
    if r:
        template += BINARY_R_OP_METHOD_TEMPLATE
    if i:
        template += BINARY_I_OP_METHOD_TEMPLATE
    return template.format(method=method, op=op)


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
    if _PY3:  # pragma: no cover
        __bytes__ = _proxy_fn(bytes)
    else:  # pragma: no cover
        __unicode__ = _proxy_fn(unicode)

    def __format__(self, format_spec):
        return format(self.__target__, format_spec)

    exec(_proxy_binary_op('lt', '<'))
    exec(_proxy_binary_op('le', '<='))
    exec(_proxy_binary_op('eq', '=='))
    exec(_proxy_binary_op('ne', '!='))
    exec(_proxy_binary_op('gt', '>'))
    exec(_proxy_binary_op('ge', '>='))

    if not _PY3:  # pragma: no cover
        def __cmp__(self, other):
            while isinstance(other, ObjectProxy):
                other = other.__target__
            return cmp(self.__target__, other)

    __hash__ = _proxy_fn(hash)

    __bool__ = _proxy_fn(bool)
    if not _PY3:  # pragma: no cover
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
        while isinstance(subclass, ObjectProxy):
            subclass = subclass.__target__
        return issubclass(subclass, self.__target__)

    def __call__(self, *args, **kwargs):
        return self.__target__(*args, **kwargs)

    __len__ = _proxy_fn(len)

    def __getitem__(self, key):
        return self.__target__[key]

    def __setitem__(self, key, value):
        self.__target__[key] = value

    def __delitem__(self, key):
        del self.__target__[key]

    __iter__ = _proxy_fn(iter)
    __reversed__ = _proxy_fn(reversed)
    __next__ = _proxy_fn(next)
    if not _PY3:  # pragma: no cover
        next = __next__
        del __next__

    def __contains__(self, item):
        return item in self.__target__

    exec(_proxy_binary_op('add', '+', r=True, i=True))
    exec(_proxy_binary_op('sub', '-', r=True, i=True))
    exec(_proxy_binary_op('mul', '*', r=True, i=True))
    exec(_proxy_binary_op('truediv', '/', r=True, i=True))
    exec(_proxy_binary_op('floordiv', '//', r=True, i=True))
    exec(_proxy_binary_op('mod', '%', r=True, i=True))
    exec(_proxy_binary_op('lshift', '<<', r=True, i=True))
    exec(_proxy_binary_op('rshift', '>>', r=True, i=True))
    exec(_proxy_binary_op('and', '&', r=True, i=True))
    exec(_proxy_binary_op('xor', '^', r=True, i=True))
    exec(_proxy_binary_op('or', '|', r=True, i=True))

    if not _PY3:  # pragma: no cover
        def __div__(self, other):
            while isinstance(other, ObjectProxy):
                other = other.__target__
            return operator.div(self.__target__, other)

    def __divmod__(self, other):
        return divmod(self.__target__, other)

    def __rdivmod__(self, other):
        return divmod(other, self.__target__)

    def __pow__(self, other, modulo=_unspecified):
        if modulo is _unspecified:
            return pow(self.__target__, other)
        else:
            while isinstance(other, ObjectProxy):
                other = other.__target__
            while isinstance(modulo, ObjectProxy):
                modulo = modulo.__target__
            return pow(self.__target__, other, modulo)

    def __rpow__(self, other):
        return pow(other, self.__target__)

    def __ipow__(self, other):
        self.__target__ **= other
        return self

    exec(_proxy_unary_op('neg', '-'))
    __abs__ = _proxy_fn(abs)
    exec(_proxy_unary_op('pos', '+'))
    exec(_proxy_unary_op('invert', '~'))

    __complex__ = _proxy_fn(complex)
    __int__ = _proxy_fn(int)
    __float__ = _proxy_fn(float)
    if not _PY3:  # pragma: no cover
        __long__ = _proxy_fn(long)
    else:  # pragma: no cover
        def __round__(self, ndigits=_unspecified):
            return round(self.__target__) if ndigits is _unspecified \
                else round(self.__target__, ndigits)

    __index__ = _proxy_fn(operator.index)

    if not _PY3:  # pragma: no cover
        __oct__ = _proxy_fn(oct)
        __hex__ = _proxy_fn(hex)

        def __coerce__(self, other):
            return coerce(self.__target__, other)
