import dl.dl_helper as h
from dl.dl_ts import calculate_mdl_for_ts
import numpy as np

# Calculate die minimal motif length for which it could be rentable
def get_min_possible_size(alphabet_size, len_ts, k_area, mdl_deviation=1.51):
    dl = h.log_2(len_ts, alphabet_size)
    for k in list(range(k_area[0], k_area[1])):
        max_possible_tss = int(len_ts/k)
        mdl_deviation_list = [mdl_deviation] * max_possible_tss
        mdl = calculate_mdl_for_ts(mdl_deviation_list, max_possible_tss, k, len_ts, alphabet_size)
        if dl > mdl:
            return k


# Dictionary, for which k-value which difference value can still be profitable at all.
# {1: -1, 2: -1, 3: -1, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1, 9: 2 ...}
def creat_dict_threshold(alphabet_size, len_sax):
    dict_threshold = {}
    for k in range(int(len_sax / 2) + 1):
        worst_case = h.log_2(k, alphabet_size)
        for i in range(k):
            mdl = h.log_2(1, len_sax) + h.log_star(i) + h.log_2(i, k) + i*2
            if mdl > worst_case:
                dict_threshold[k] = (i - 1)
                break
    return dict_threshold


def get_best_pattern(list_of_pattern):
    mdl_min = np.inf
    for i in list_of_pattern:
        if list_of_pattern[i]["mdl"] < mdl_min:
            indexes = list_of_pattern[i]["indexes"]
            mdl_min = list_of_pattern[i]["mdl"]
    return indexes