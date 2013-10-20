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

import unittest

from pyoxy import *


try:  # pragma: no cover
    unicode
    PY3 = False
except NameError:  # pragma: no cover
    PY3 = True


class Object(object):
    pass


class ObjectProxyTest(unittest.TestCase):

    def test_attr(self):
        o = Object()
        o.attr = 1
        p = ObjectProxy(o)
        self.assertEqual(1, p.attr)
        o.attr = 2
        self.assertEqual(2, p.attr)
        self.assertEqual(2, o.attr)
        p.attr = 3
        self.assertEqual(3, p.attr)
        self.assertEqual(3, o.attr)
        del o.attr
        with self.assertRaises(AttributeError):
            p.attr
        with self.assertRaises(AttributeError):
            o.attr
        p.attr = 1
        self.assertEqual(1, p.attr)
        self.assertEqual(1, o.attr)
        del p.attr
        with self.assertRaises(AttributeError):
            p.attr
        with self.assertRaises(AttributeError):
            o.attr

    def test_attr_target(self):
        o = Object()
        o.id = id(o)
        p = ObjectProxy()
        with self.assertRaises(AttributeError):
            p.__target__
        p.__target__ = o
        self.assertEqual(o, p.__target__)
        self.assertEqual(o.id, p.id)
        del p.__target__
        with self.assertRaises(AttributeError):
            p.__target__
        with self.assertRaises(AttributeError):
            self.assertEqual(None, p.id)

    def test_dir(self):
        o = Object()
        o.attr = 1
        dir_p = dir(ObjectProxy(o))
        self.assertTrue(set(dir(o)).issubset(set(dir_p)))
        self.assertIn('__target__', dir_p)

    def test_str_repr(self):
        p = ObjectProxy(12)
        self.assertEqual(repr(12), repr(p))
        self.assertEqual(str(12), str(p))
        if PY3:  # pragma: no cover
            with self.assertRaises(AttributeError):
                p.__unicode__
            self.assertEqual(bytes(12), bytes(p))
        else:  # pragma: no cover
            with self.assertRaises(AttributeError):
                p.__bytes__
            self.assertEqual(unicode(12), unicode(p))
        self.assertEqual(format(12), format(p))
        self.assertEqual(format(12, '+'), format(p, '+'))

    def test_comparison(self):
        p11 = ObjectProxy(11)
        p12 = ObjectProxy(12)
        self.assertTrue(p11 < p12)
        self.assertTrue(p11 <= p12)
        self.assertTrue(p11 == p11)
        self.assertTrue(p11 != p12)
        self.assertTrue(p12 > p11)
        self.assertTrue(p12 >= p11)
        self.assertFalse(p11 > p12)
        self.assertFalse(p11 >= p12)
        self.assertFalse(p11 != p11)
        self.assertFalse(p11 == p12)
        self.assertFalse(p12 < p11)
        self.assertFalse(p12 <= p11)
        if not PY3:  # pragma: no cover
            self.assertEqual(0, cmp(p11, 11))
            self.assertEqual(0, cmp(p11, p11))
            self.assertEqual(1, cmp(p12, 11))
            self.assertEqual(1, cmp(p12, p11))
            self.assertEqual(-1, cmp(p11, 12))
            self.assertEqual(-1, cmp(p11, p12))

    def test_hash(self):
        self.assertEqual(hash(12), hash(ObjectProxy(12)))

    def test_bool(self):
        self.assertFalse(ObjectProxy(False))
        self.assertTrue(ObjectProxy(True))
