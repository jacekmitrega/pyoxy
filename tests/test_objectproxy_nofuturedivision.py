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

from __future__ import unicode_literals  # no division here

import unittest

from pyoxy import ObjectProxy as OP


try:  # pragma: no cover
    unicode
    _PY3 = False
except NameError:  # pragma: no cover
    _PY3 = True


class ObjectProxyNoFutureDivisionTest(unittest.TestCase):

    def check_result(self, expected_result, result,
                     assert_result_is_proxy=False):
        self.assertEqual(expected_result, result)
        self.assertEqual(assert_result_is_proxy, isinstance(result, OP))

    def test_div(self):
        exp = 2 / 3
        self.check_result(exp, OP(2) / 3)
        self.check_result(exp, OP(2) / OP(3))
        self.check_result(exp, OP(2) / OP(OP(3)))
        self.check_result(exp, OP(OP(2)) / OP(OP(3)))
        self.check_result(exp, OP(OP(OP(2))) / OP(OP(3)))

    def test_div_error(self):
        # This test fails in Python 2, passes in Python 3.
        # There is no reverse operator magic method for old division
        # and naturally int's div implementation doesn't support the proxy.
        # The workaround is to wrap the 1st operand in ObjectProxy,
        # like in the example above in test_div.
        self.check_result(2 / 3, 2 / OP(3))
    if not _PY3:  # pragma: no cover
        test_div_error = unittest.expectedFailure(test_div_error)

    def test_floordiv(self):
        exp = 8 // 3
        self.check_result(exp, OP(8) // OP(3))
        self.check_result(exp, 8 // OP(3))
        self.check_result(exp, OP(8) // 3)
        self.check_result(exp, OP(OP(8)) // OP(OP(3)))
