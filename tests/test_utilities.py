import unittest

from utilities import extended_euclidean, greatest_common_divisor, mod_inverse, letters_only_uppercase


class TestUtilities(unittest.TestCase):

    def test_greatest_common_divisor(self):
        self.assertEqual(greatest_common_divisor(16, 12), 4)
        self.assertEqual(greatest_common_divisor(14, 8), 2)
        self.assertEqual(greatest_common_divisor(3, 6), 3)
        self.assertEqual(greatest_common_divisor(9, 9), 9)
        self.assertEqual(greatest_common_divisor(12, 13), 1)

    def test_extended_euclidean(self):
        self.assertEqual(extended_euclidean(16, 12), (4, 1, -1))
        self.assertEqual(extended_euclidean(14, 8), (2, -1, 2))
        self.assertEqual(extended_euclidean(3, 6), (3, 1, 0))
        self.assertEqual(extended_euclidean(9, 9), (9, 0, 1))
        self.assertEqual(extended_euclidean(12, 13), (1, -1, 1))

    def test_mod_inverse(self):
        self.assertEqual(mod_inverse(2, 26), None)
        self.assertEqual(mod_inverse(15, 26), 7)
        self.assertEqual(mod_inverse(26, 8), None)
        self.assertEqual(mod_inverse(5, 18), 11)
        self.assertEqual(mod_inverse(12, 3), None)

    def test_letters_only_uppercase(self):
        self.assertEqual(letters_only_uppercase("abcd"), "ABCD")
        self.assertEqual(letters_only_uppercase("ab 123 cd"), "ABCD")

        self.assertEqual(letters_only_uppercase("Hello World"), "HELLOWORLD")
        self.assertEqual(letters_only_uppercase("h0e0l0l0o0W0o0r0l0d0"), "HELLOWORLD")

        self.assertEqual(letters_only_uppercase("1243!@£$"), "")
        self.assertEqual(letters_only_uppercase(""), "")
