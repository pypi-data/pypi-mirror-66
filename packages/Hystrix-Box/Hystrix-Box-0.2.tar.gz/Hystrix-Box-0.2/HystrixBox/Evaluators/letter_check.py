import re
from collections import Counter
from HystrixBox.Evaluators.Evaluator import Evaluator
# https://crypto.stackexchange.com/questions/30209/developing-algorithm-for-detecting-plain-text-via-frequency-analysis
ENGLISH_FREQUENCIES = {'e': 12.02, 't': 9.1, 'a': 8.12, 'o': 7.68, 'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02,
                       'h': 5.92,
                       'd': 4.32, 'l': 3.98, 'u': 2.88,
                       'c': 2.71, 'm': 2.61, 'f': 2.30, 'y': 2.11, 'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49,
                       'v': 1.11,
                       'k': 0.69, 'x': 0.17, 'q': 0.11, 'j': 0.10, 'z': 0.07}


def Frequency_Analysis(chipertext):
    # Remove Non alphabetic charts
    r2 = re.compile(r'[^a-zA-Z]', re.MULTILINE)
    chipertext = r2.sub('', chipertext)
    # All to lower case
    chipertext = chipertext.lower()

    # Get frequencies
    frequencies = Counter(chipertext).most_common()
    # Make frequencies to percentages
    percentages = [(letter, count / len(chipertext) * 100) for letter, count in frequencies]
    return percentages


def getChi2(percentages):
    error = 0
    for observation in percentages:
        letter = observation[0]
        obs = observation[1]
        exp = ENGLISH_FREQUENCIES[letter]
        error += (pow((obs - exp), 2) / exp)
    return error


class LetterEvaluator(Evaluator):
    """
        A class used to represent a letter analysis evaluator.

        Score based the difference between the English letter's frequencies and the plaintext letter's frequencies
    """
    @staticmethod
    def evaluate(text):
        percentages = Frequency_Analysis(text)
        error = getChi2(percentages)
        return error

