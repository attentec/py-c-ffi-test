import os
import unittest

import pydffi

_HERE = os.path.dirname(os.path.abspath(__file__))

class TestCFFI(unittest.TestCase):
    def test_it(self):
        pydffi.dlopen(_HERE + '/library.so')
        FFI = pydffi.FFI()
        CU = FFI.cdef('#include "{}/library.h"'.format(_HERE))

        foo = CU.types.Foo(bar=1)
        CU.funcs.by_ptr(FFI.ptr(foo))
        self.assertEqual(foo.bar, 2);

if __name__ == '__main__':
    unittest.main()