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

import abc
import unittest

from pyoxy import ObjectProxy as OP


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
        p = OP(o)
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
        p = OP()
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
        dir_p = dir(OP(o))
        self.assertTrue(set(dir(o)).issubset(set(dir_p)))
        self.assertIn('__target__', dir_p)

    def test_descriptor(self):
        class TestDescriptor(object):
            def __get__(self, instance, owner):
                return instance._d

            def __set__(self, instance, value):
                instance._d = value

            def __delete__(self, instance):
                del instance._d

        class TestClass(object):
            d = OP(TestDescriptor())

        o = TestClass()
        o.d = 1
        self.assertEqual(1, o.d)
        self.assertEqual(1, o._d)
        del o.d
        with self.assertRaises(AttributeError):
            o.d
        with self.assertRaises(AttributeError):
            o._d

    def test_str_repr(self):
        p = OP(12)
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
        p11 = OP(11)
        p12 = OP(12)
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
        self.assertEqual(hash(12), hash(OP(12)))

    def test_bool(self):
        self.assertFalse(OP(False))
        self.assertTrue(OP(True))

    def create_test_isinstance(mixin_meta=type):
        """
        Create isinstance tests with varying metaclasses.

        abc.ABCMeta metaclass affects isinstance and issubclass.

        """
        def test_isinstance(self):
            class Mixin(object):
                __metaclass__ = mixin_meta

            class SubObject(Mixin, Object):
                pass

            class SubSubObject(SubObject):
                pass

            o = SubObject()
            p = OP(o)
            self.assertEqual(isinstance(o, object),
                             isinstance(p, object))
            self.assertEqual(isinstance(o, Mixin),
                             isinstance(p, Mixin))
            self.assertEqual(isinstance(o, Object),
                             isinstance(p, Object))
            self.assertEqual(isinstance(o, SubObject),
                             isinstance(p, SubObject))
            self.assertEqual(isinstance(o, SubSubObject),
                             isinstance(p, SubSubObject))
            self.assertEqual(isinstance(o, int),
                             isinstance(p, int))

            self.assertFalse(isinstance(o, OP))
            self.assertTrue(isinstance(p, OP))

            self.assertFalse(isinstance(o, OP(OP)))
            self.assertTrue(isinstance(o, OP(object)))
            self.assertTrue(isinstance(o, OP(Mixin)))
            self.assertTrue(isinstance(o, OP(Object)))
            self.assertTrue(isinstance(o, OP(SubObject)))
            self.assertFalse(isinstance(o, OP(SubSubObject)))
            self.assertFalse(isinstance(o, OP(int)))

            self.assertTrue(isinstance(p, OP(OP)))
            self.assertTrue(isinstance(p, OP(object)))
            self.assertTrue(isinstance(p, OP(Mixin)))
            self.assertTrue(isinstance(p, OP(Object)))
            self.assertTrue(isinstance(p, OP(SubObject)))
            self.assertFalse(isinstance(p, OP(SubSubObject)))
            self.assertFalse(isinstance(p, OP(int)))

            self.assertTrue(isinstance(p, OP(OP(OP))))
            self.assertTrue(isinstance(p, OP(OP(SubObject))))
            self.assertFalse(isinstance(p, OP(OP(SubSubObject))))

            with self.assertRaises(AttributeError):
                isinstance(p, OP())

        return test_isinstance
    test_isinstance_no_abcmeta = create_test_isinstance()
    test_isinstance_abcmeta = create_test_isinstance(mixin_meta=abc.ABCMeta)

    def create_test_issubclass(mixin_meta=type):
        """
        Create issubclass tests with varying metaclasses.

        abc.ABCMeta metaclass affects isinstance and issubclass.

        """
        def test_issubclass(self):
            class Mixin(object):
                __metaclass__ = mixin_meta

            class SubObject(Mixin, Object):
                pass

            class SubSubObject(SubObject):
                pass

            o = SubObject
            p = OP(o)
            self.assertEqual(issubclass(o, object),
                             issubclass(p, object))
            self.assertEqual(issubclass(o, Mixin),
                             issubclass(p, Mixin))
            self.assertEqual(issubclass(o, Object),
                             issubclass(p, Object))
            self.assertEqual(issubclass(o, SubSubObject),
                             issubclass(p, SubSubObject))
            self.assertEqual(issubclass(o, int),
                             issubclass(p, int))

            self.assertEqual(issubclass(object, o),
                             issubclass(object, p))
            self.assertEqual(issubclass(Mixin, o),
                             issubclass(Mixin, p))
            self.assertEqual(issubclass(Object, o),
                             issubclass(Object, p))
            self.assertEqual(issubclass(SubObject, o),
                             issubclass(SubObject, p))
            self.assertEqual(issubclass(SubSubObject, o),
                             issubclass(SubSubObject, p))
            self.assertEqual(issubclass(int, o),
                             issubclass(int, p))

            self.assertFalse(issubclass(o, OP))
            self.assertFalse(issubclass(p, OP))

            self.assertFalse(issubclass(o, OP(OP)))
            self.assertTrue(issubclass(o, OP(object)))
            self.assertTrue(issubclass(o, OP(Mixin)))
            self.assertTrue(issubclass(o, OP(Object)))
            self.assertTrue(issubclass(o, OP(SubObject)))
            self.assertFalse(issubclass(o, OP(SubSubObject)))
            self.assertFalse(issubclass(o, OP(int)))

            self.assertFalse(issubclass(p, OP(OP)))
            self.assertTrue(issubclass(p, OP(object)))
            self.assertTrue(issubclass(p, OP(Mixin)))
            self.assertTrue(issubclass(p, OP(Object)))
            self.assertFalse(issubclass(p, OP(SubSubObject)))
            self.assertFalse(issubclass(p, OP(int)))

            self.assertFalse(issubclass(p, OP(OP(OP))))
            self.assertFalse(issubclass(p, OP(OP(SubSubObject))))

            with self.assertRaises(AttributeError):
                issubclass(p, OP())

            if mixin_meta == abc.ABCMeta and not PY3:  # pragma: no cover
                # In Python 2.x, if class' metaclass is ABCMeta, the following
                # works without 'test_issubclass_error_workaround()':
                self.assertTrue(issubclass(p, SubObject))
                self.assertTrue(issubclass(p, OP(SubObject)))
                self.assertTrue(issubclass(p, OP(OP(SubObject))))
                # In other cases it breaks as in test_issubclass_error() test.
                # Check test_issubclass_error_workaround() below.

        return test_issubclass
    test_issubclass_no_abcmeta = create_test_issubclass()
    test_issubclass_abcmeta = create_test_issubclass(mixin_meta=abc.ABCMeta)

    @unittest.expectedFailure
    def test_issubclass_error(self):
        # Doesn't work because Object's metaclass doesn't have proxy aware
        # __subclasscheck__ method defined.
        # Check test_issubclass_error_workaround() below.
        self.assertTrue(issubclass(OP(Object), Object))

    def test_issubclass_error_workaround(self):
        # This is a workaround for test_issubclass_error() problem above.
        # Proxying 2nd parameter makes issubclass() function call proxy aware
        # OP.__subclasscheck__() method.
        self.assertTrue(issubclass(OP(Object), OP(Object)))

    def test_call(self):
        self.assertEqual(0, OP(lambda: 0)())
        self.assertEqual(1, OP(lambda p1: p1)(1))
        self.assertEqual((1, 2), OP(lambda p1, p2: (p1, p2))(1, 2))
        self.assertEqual((1, 2), OP(lambda p1, p2: (p1, p2))(p1=1, p2=2))
        self.assertEqual((1, 2), OP(lambda *args, **kwargs: args)(1, 2))
        self.assertEqual({'p1': 1, 'p2': 2},
                         OP(lambda *args, **kwargs: kwargs)(p1=1, p2=2))
