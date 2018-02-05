import math
import os
from utilities import letters_only_uppercase


# get the ngram data folder
NGRAM_DATA_PATH = os.path.dirname(os.path.realpath(__file__)) + "/ngram_data/"
# cache ngram data so it does not have to be reloaded every time
_cached_ngram_data = {}


class NgramData:

    def __init__(self, n):
        self.n = n

        # check if the path exists
        path = NGRAM_DATA_PATH + str(n) + "GRAM.txt"
        if not os.path.isfile(path):
            raise ValueError("Ngram data does not exist for n={}".format(n))
        # read data
        total_count = 0
        frequencies = {}
        with open(path, "r") as f:
            for line in f:
                # split into each line into the key and the count
                key, count_str = line.split(" ")
                # check the key is n long
                if len(key) != n:
                    raise ValueError
                # store the frequency
                frequency = int(count_str)
                frequencies[key] = frequency
                total_count += frequency
        # now calculate the scores now that the total_count is known
        self.scores = {}
        self.score_other = -math.log10(1 / total_count)
        sum_frequency_times_score = 0  # used to calculate the average
        for key, frequency in frequencies.items():
            score = -math.log10(frequency / total_count)
            self.scores[key] = score
            sum_frequency_times_score += frequency * score
        # calculate the average. The closer text is to this, the better
        self.avg = sum_frequency_times_score / total_count

    def get_score(self, key):
        """Get the score for a specific key"""
        # check the specified key is length n
        if len(key) != self.n:
            raise ValueError("len(key) != n. {} != {}".format(len(key), self.n))
        # retrieve the score. if the key is not present, return score_other
        return self.scores.get(key, self.score_other)

    def rate(self, text):
        """Rate how close to English text some text is. Score of 0 is closest to English text."""
        # strip all non letter characters
        letters = letters_only_uppercase(text)
        # check it is at least n long
        if len(letters) < self.n:
            return 0
        # calculate the total score and the number of patterns
        total_score = 0
        num_patterns = len(letters) - self.n + 1
        # cache variables in local scope to speed up access
        n = self.n
        scores = self.scores
        score_other = self.score_other
        for i in range(num_patterns):
            try:
                total_score += scores[letters[i:i+n]]
            except KeyError:
                total_score += score_other
        # calculate the average score
        average_score = total_score / num_patterns
        # return how close the average_score of the text is to the average score of the dataset.
        return abs(self.avg - average_score)


def get_ngram_data(n):
    """Returns the instance of NgramData containing Ngrams of length n. Caches the instances so the data doesn't have to be repeatedly loaded from disk"""
    global _cached_ngram_data
    if n not in _cached_ngram_data:
        _cached_ngram_data[n] = NgramData(n)
    return _cached_ngram_data[n]


def rate(text, n=4):
    """Shortcut for get_ngram_data(n).rate(text)"""
    ngram_data = get_ngram_data(n)
    return ngram_data.rate(text)
