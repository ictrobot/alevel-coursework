# The options to be passed into a tkinter label to make it look like a title.
TITLE_LABEL_OPTIONS = {"font": (None, 20)}
SUBTITLE_LABEL_OPTIONS = {"font": (None, 14)}


def greatest_common_divisor(a, b):
    """Returns the greatest common divisor of a & b"""
    while a != 0:
        a, b = b % a, a
    return b


def extended_euclidean(a, b):
    """The Extended Euclidean Algorithm, required for finding the modular inverse"""
    # from: https://anh.cs.luc.edu/331/notes/xgcd.pdf
    prevx, x = 1, 0
    prevy, y = 0, 1
    while b != 0:
        q = a // b
        x, prevx = prevx - q*x, x
        y, prevy = prevy - q*y, y
        a, b = b, a % b
    return a, prevx, prevy


def mod_inverse(a, b):
    """Returns the modular inverse of a & b"""
    gcd, prevx, prevy = extended_euclidean(a, b)
    if gcd != 1:
        # no mod inverse if a & b aren't coprime
        return None
    return prevx % b
