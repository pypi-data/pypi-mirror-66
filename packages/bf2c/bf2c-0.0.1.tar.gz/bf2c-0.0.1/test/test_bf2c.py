from unittest import TestCase

import os

from bf2c.bf2c import BFConverter

BF = ',[[>+>+<<-]>>[<<+>>-]<<-]>.<'


class TestBF2C(TestCase):
    def test_convert_to_c(self):
        BFConverter().convert2file('test', BF)
        self.assertTrue(os.path.exists('test.c'), 'Should create test.c file.')
        os.remove('test.c')

    def test_convert_to_cpp(self):
        BFConverter(language='cpp').convert2file('test', BF)
        self.assertTrue(os.path.exists('test.cpp'), 'Should create test.cpp file.')
        os.remove('test.cpp')

    def test_compile(self):
        BFConverter().compile('test', BF)
        self.assertTrue(os.path.exists('test.c'), 'Should create test.c file.')
        self.assertTrue(os.path.exists('test.exe'), 'Should create test.exe file.')
        os.remove('test.c')
        #os.remove('test.exe')

    def test_language(self):
        b = BFConverter()
        self.assertEqual(b.language, 'c', 'Default language should be C.')
        b.language = 'cpp'
        self.assertEqual(b.language, 'cpp', 'Should be changed to C++.')
        b.language = 'c'
        self.assertEqual(b.language, 'c', 'Should be changed back to C.')

        def f(*args):
            nonlocal b
            b.language = 'java'

        self.assertRaises(ValueError, f, 'Should raise Value Error.')
