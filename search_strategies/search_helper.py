def create_word_lists(x, k):
    words = []
    for i in range(len(x) - k + 1):
        words.append("".join(x[i: i + k]))
    return words