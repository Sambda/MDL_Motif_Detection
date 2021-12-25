from overlappings.pulp_list import get_optimized_list_with_pulp
import params as p
from itertools import groupby
import numpy as np
from dl.dl_helper import get_difference_array_double, calc_mdl_for_distance_array

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


# Build matrix with values of all mdl values per possible center, take the cheapest combination
def calc_mdl_for_all_possible_centers(diff1, diff2, mdl):
    len_mdl = len(mdl)
    diff1 = [j for i in diff1 for j in i]
    diff2 = [j for i in diff2 for j in i]
    a = np.zeros(shape=(len_mdl, len_mdl))
    a[0] = np.array(mdl)
    a[:, 0] = np.array(mdl)
    np.fill_diagonal(a, 1.51)

    list_zero = np.argwhere(a == 0)
    k = len(diff1[0])
    for i in list_zero[:int(len(list_zero) / 2)]:
        difference_array = get_difference_array_double(diff1[i[0]], diff2[i[0]], diff1[i[1]], diff2[i[1]])
        sum_of_position_of_changes = k - difference_array.count(0)
        mdl_val = 1.51 if sum_of_position_of_changes == 0 else calc_mdl_for_distance_array(sum_of_position_of_changes, k,
                                                                                           difference_array)
        a[i[0], i[1]] = mdl_val
        a[i[1], i[0]] = mdl_val

    res = [sum(e) for e in a]
    return a[res.index(min(res))]



# Get list with the best non-overlapping candidates
def get_small_candidate_list(index_list, mdl_deviation_list, s):
    candidate = [0] * len(s.words)
    mdl_deviation = candidate.copy()
    for ind, mdl in zip(index_list, mdl_deviation_list):
        candidate[ind[0]] = 1
        mdl_deviation[ind[0]] = mdl
    pattern_list, pattern_list_numeric, pattern_list_numeric_2, index_list, mdl_deviation_list \
        = get_optimized_list_with_pulp(s.words, candidate, mdl_deviation, s.words_numeric, s.words_numeric_2)
    return pattern_list, pattern_list_numeric, pattern_list_numeric_2, index_list, mdl_deviation_list


def remove_overlapping(candidate_list, index_list, mld_list,s, motifs):
    if len(candidate_list) > 0:
        for pattern_list, index_list, mdl_deviation_list in zip(candidate_list, index_list, mld_list):
            # If length of possible motifs > 2 remove overlapping
            if len(pattern_list) != 2:
                # Check if all pattern overlap with each other -> If true take cheapest one
                for ind in index_list[2:]:
                    if index_list[1][1] > ind[0]:
                        all_overlapping = True
                    else:
                        all_overlapping = False
                        break
                if all_overlapping:
                    index_min_dev = mdl_deviation_list[1:].index(min(mdl_deviation_list[1:])) + 1
                    pattern_list = [pattern_list[0], pattern_list[index_min_dev]]
                    index_list = [index_list[0], index_list[index_min_dev]]
                    mdl_deviation_list = [mdl_deviation_list[0], mdl_deviation_list[index_min_dev]]

                # Use optimizer to get the get combination of pattern
                else:
                    pattern_list, pattern_list_numeric, pattern_list_numeric_2, index_list, mdl_deviation_list = \
                        get_small_candidate_list(index_list, mdl_deviation_list, s)
                    # Check if another pattern as center would be cheaper
                    if p.check_if_other_center_would_be_better:
                        if not all_equal(mdl_deviation_list):
                            mdl_deviation_list = calc_mdl_for_all_possible_centers(pattern_list_numeric,
                                                                                     pattern_list_numeric_2, mdl_deviation_list)

            if len(pattern_list) > 1:
                motifs.set_lists(s.k, pattern_list, index_list, mdl_deviation_list)
    return motifs