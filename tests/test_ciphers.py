import unittest

from ciphers.affine import affine, reverse_affine
from ciphers.caesar import caesar
from ciphers.scytale import reverse_scytale, scytale
from ciphers.substitution import substitution
from ciphers.vigenere import vigenere, string_to_shifts, reverse_vigenere


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

    def test_vigenere(self):
        self.assertEqual(vigenere("Attack at dawn", [11, 4, 12, 14, 13]), "Lxfopv ef rnhr")
        self.assertEqual(vigenere("Interwoven Caesar ciphers", [21, 8, 6, 4, 13, 4, 17, 4]), "Dvzieafzzv Ierwrv xqvlrvj")

        with self.assertRaises(ValueError) as context:
            vigenere("No shifts", [])

    def test_reverse_vigenere(self):
        self.assertEqual(reverse_vigenere("Lxfopv ef rnhr", [11, 4, 12, 14, 13]), "Attack at dawn")
        self.assertEqual(reverse_vigenere("Dvzieafzzv Ierwrv xqvlrvj", [21, 8, 6, 4, 13, 4, 17, 4]), "Interwoven Caesar ciphers")

    def test_string_to_shifts(self):
        self.assertEqual(string_to_shifts("Lemon"), [11, 4, 12, 14, 13])
        self.assertEqual(string_to_shifts("Vigenere"), [21, 8, 6, 4, 13, 4, 17, 4])

    def test_substitution(self):
        self.assertEqual(substitution("Hello", {"H": "A", "E": "B", "L": "C", "O": "D"}), "abccd")
        self.assertEqual(substitution("Substitution", {"S": "Q", "U": "E", "B": "T", "T": "U", "I": "A", "O": "D", "N": "G"}), "qetquaueuadg")
