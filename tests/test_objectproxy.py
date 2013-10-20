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
