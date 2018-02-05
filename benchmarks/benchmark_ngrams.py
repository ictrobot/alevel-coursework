from benchmark import benchmark
from ngrams import NgramData
from benchmark_letters_only import string_translate_defaultdict as letters_only

###############################################################################


class Current(NgramData):

    def rate(self, text):
        # Current implementation
        letters = ""
        for letter in text.upper():
            if 65 <= ord(letter) <= 90:
                letters += letter
        if len(letters) < self.n:
            return 0
        total_score = 0
        num_patterns = len(letters) - self.n + 1
        for i in range(num_patterns):
            key = letters[i:i + self.n]
            total_score += self.get_score(key)
        average_score = total_score / num_patterns
        return abs(self.avg - average_score)

###############################################################################


class InlineDictGet(NgramData):

    def rate(self, text):
        # uses self.scores.get(...) instead of self.get_score(...) to reduce function overhead
        letters = ""
        for letter in text.upper():
            if 65 <= ord(letter) <= 90:
                letters += letter
        if len(letters) < self.n:
            return 0
        total_score = 0
        num_patterns = len(letters) - self.n + 1
        for i in range(num_patterns):
            key = letters[i:i + self.n]
            total_score += self.scores.get(key, self.score_other)
        average_score = total_score / num_patterns
        return abs(self.avg - average_score)

###############################################################################


class DictKeyError(NgramData):

    def rate(self, text):
        # tries to read the pattern for the dictionary, if its not there catch KeyError and add score_other (instead of using .get() where you can supply a default)
        letters = ""
        for letter in text.upper():
            if 65 <= ord(letter) <= 90:
                letters += letter
        if len(letters) < self.n:
            return 0
        total_score = 0
        num_patterns = len(letters) - self.n + 1
        for i in range(num_patterns):
            key = letters[i:i + self.n]
            try:
                total_score += self.scores[key]
            except KeyError:
                total_score += self.score_other
        average_score = total_score / num_patterns
        return abs(self.avg - average_score)

###############################################################################


class LocalVarDictKeyError(NgramData):

    def rate(self, text):
        # saves the n, scores & score_other variables into the function scope to avoid object scope lookups, as well as using keyerror instead of .get()
        letters = ""
        for letter in text.upper():
            if 65 <= ord(letter) <= 90:
                letters += letter
        n = self.n
        scores = self.scores
        score_other = self.score_other
        if len(letters) < self.n:
            return 0
        total_score = 0
        num_patterns = len(letters) - n + 1
        for i in range(num_patterns):
            key = letters[i:i + n]
            try:
                total_score += scores[key]
            except KeyError:
                total_score += score_other
        average_score = total_score / num_patterns
        return abs(self.avg - average_score)

###############################################################################


class LocalVarDictKeyErrorLettersOnly(NgramData):

    def rate(self, text):
        # uses the best letters_only function from the benchmarks, saves variables locally & uses keyerror instead of .get()
        letters = letters_only(text)
        n = self.n
        scores = self.scores
        score_other = self.score_other
        if len(letters) < self.n:
            return 0
        total_score = 0
        num_patterns = len(letters) - n + 1
        for i in range(num_patterns):
            key = letters[i:i + n]
            try:
                total_score += scores[key]
            except KeyError:
                total_score += score_other
        average_score = total_score / num_patterns
        return abs(self.avg - average_score)

###############################################################################


if __name__ == "__main__":
    # read in the sample text
    with open("sample.txt", "r") as f:
        text = f.read().strip()
    # list of the instances to test
    instances = [Current(4), InlineDictGet(4), DictKeyError(4), LocalVarDictKeyError(4), LocalVarDictKeyErrorLettersOnly(4)]
    # test the instances
    correct = Current(4).rate("Hello World")
    for inst in instances:
        if inst.rate("Hello World") != correct:
            print("Function {} FAILED".format(inst.__class__.__name__))
            exit(1)
        else:
            print("Function {} passed".format(inst.__class__.__name__))
    # benchmark the instances
    for length in (4, 10, 100, 1000, 10000, 100000):
        # get text of the right length and print header
        test_text = text[:length]
        print("\n{:,} long string".format(length))
        for inst in instances:
            # benchmark each function, using the class name as the name to be printed
            name = inst.__class__.__name__
            benchmark(inst.rate, name=name, args=[test_text])
