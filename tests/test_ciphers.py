import unittest

from ciphers.affine import affine, reverse_affine
from ciphers.caesar import caesar
from ciphers.scytale import reverse_scytale, scytale


class TestCiphers(unittest.TestCase):

    def test_caesar(self):
        self.assertEqual(caesar("Hello World", 11), "Spwwz Hzcwo")
        self.assertEqual(caesar("Caesar Cipher is a monoalphabetic substitution cipher", 17), "Trvjri Tzgyvi zj r dfefrcgyrsvkzt jlsjkzklkzfe tzgyvi")

    def test_caesar_reverse(self):
        self.assertEqual(caesar("Spwwz Hzcwo", -11), "Hello World")
        self.assertEqual(caesar("Trvjri Tzgyvi zj r dfefrcgyrsvkzt jlsjkzklkzfe tzgyvi", -17), "Caesar Cipher is a monoalphabetic substitution cipher")

    def test_scytale(self):
        self.assertEqual(scytale("TranspositionCiphers", 5), "TpiproohasneniCrstis")
        self.assertEqual(scytale("AncientGreeks", 4), "Aersnne_cte_iGk_")

    def test_scytale_reverse(self):
        self.assertEqual(reverse_scytale("TpiproohasneniCrstis", 5), "TranspositionCiphers")
        self.assertEqual(reverse_scytale("Aersnne_cte_iGk_", 4), "AncientGreeks")

    def test_affine(self):
        self.assertEqual(affine("Hello World", 9, 5), "Qpaab Vbcag")
        self.assertEqual(affine("Affine Cipher", 11, 7), "Hkkruz Drqgzm")

    def test_affine_reverse(self):
        self.assertEqual(reverse_affine("Qpaab Vbcag", 9, 5), "Hello World")
        self.assertEqual(reverse_affine("Hkkruz Drqgzm", 11, 7), "Affine Cipher")
