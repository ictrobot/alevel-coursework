import unittest

from ciphers.caesar import caesar


class TestCiphers(unittest.TestCase):

    def test_caesar(self):
        self.assertEqual(caesar("Hello World", 11), "Spwwz Hzcwo")
        self.assertEqual(caesar("Caesar Cipher is a monoalphabetic substitution cipher", 17), "Trvjri Tzgyvi zj r dfefrcgyrsvkzt jlsjkzklkzfe tzgyvi")

    def test_caesar_reverse(self):
        self.assertEqual(caesar("Spwwz Hzcwo", -11), "Hello World")
        self.assertEqual(caesar("Trvjri Tzgyvi zj r dfefrcgyrsvkzt jlsjkzklkzfe tzgyvi", -17), "Caesar Cipher is a monoalphabetic substitution cipher")
