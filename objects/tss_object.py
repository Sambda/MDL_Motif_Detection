def create_word_lists(x, k):
    words = []
    for i in range(len(x) - k + 1):
        words.append("".join(x[i: i + k]))
    return words


def set_subsequence_object(k, series):
    subsequence = Subsequences(k)
    subsequence.words = create_word_lists(series.sax, k)
    subsequence.words_numeric = create_word_lists(series.sax_numeric, k)
    subsequence.words_numeric_2 = create_word_lists(series.sax_numeric_2, k) if series.double else []
    return subsequence


class Subsequences(object):
    def __init__(self, k=[], words: list = [], words_numeric: list = [], words_numeric_2: list =[]):
        self.k = k
        self.words = words
        self.words_numeric = words_numeric
        self.words_numeric_2 = words_numeric_2
        self.candidate_list = []
        self.index_list = []
        self.mld_list = []

    def set_lists(self, candidate, index, mld):
        self.candidate_list = candidate
        self.index_list = index
        self.mld_list = mld