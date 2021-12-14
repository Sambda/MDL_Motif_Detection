import numpy as np
import dl.dl_helper as dl_helper
import params as p


def mdl_for_candidate_list(subsequence, series):
    k = subsequence.k
    pattern_list_all, index_list_all, mdl_deviation_list_all = [], [], []

    # Bad encoding for compairing with MDL
    exp_way = dl_helper.log_2(subsequence.k, series.alphabet_size)

    # Location of pattern + Indicatorbit
    alphabet_size_mdl_cost = dl_helper.log_2(1, series.len_sax) #+ 1

    # Mdl cost if difference is 0
    mdl_for_zero_difference = 1.51

    # If a word already is in candidate list with dist 0 to target word not necessary to look at it again, skip it.
    indexes_to_skip = []

    word_1_index_before = 0
    word_1_mdl_sum_before = np.inf
    word_1_len_candidate_list_before = 0

    sum_of_position_of_changes_old = np.inf
    index_2_to_skip = 0

    for index_1, word_1 in enumerate(subsequence.words[:-1]):
        pattern_list = []
        if index_1 not in indexes_to_skip:

            if "W" not in subsequence.words_numeric[index_1]:
                # Add target candidate to list
                pattern_list = [word_1]
                index_list = [[index_1, index_1 + k]]
                mdl_deviation_list = [mdl_for_zero_difference]

                start_pos = index_1 + k
                end_pos = len(subsequence.words)

                for index_2 in range(start_pos, end_pos):
                    index_2 = index_2 + index_2_to_skip * k
                    if index_2 < end_pos:
                        if "W" not in subsequence.words_numeric[index_2]:

                            # Sum of difference between word_1 and word_2
                            difference_array = dl_helper.get_difference_array_double(subsequence.words_numeric[index_1], subsequence.words_numeric_2[index_1], subsequence.words_numeric[index_2],
                                                                                     subsequence.words_numeric_2[index_2]) \
                                if p.double_sax else dl_helper.get_difference_array(subsequence.words_numeric[index_1], subsequence.words_numeric[index_2])

                            # On how many positions something have to be changed
                            #sum_of_position_of_changes = k - difference_array.count(0)
                            sum_of_position_of_changes = k - np.count_nonzero(difference_array == 0)
                            # Only got further if sum of position changes is under threshold
                            # TODO threshold
                            # if sum_of_position_of_changes <= series.dict_threshold[k]:

                            if sum_of_position_of_changes == 0:
                                indexes_to_skip.append(index_2)
                                mdl_now = mdl_for_zero_difference
                            else:
                                mdl_now = dl_helper.calc_mdl_for_distance_array(sum_of_position_of_changes, k, difference_array)

                            if mdl_now + alphabet_size_mdl_cost < exp_way:

                                if index_2 - index_list[-1][0] == 1:
                                    if mdl_now >= mdl_deviation_list[-1]:
                                        pass
                                    else:
                                        pattern_list.append(subsequence.words[index_2])
                                        index_list.append([index_2, index_2 + k])
                                        mdl_deviation_list.append(mdl_now)

                                        if sum_of_position_of_changes_old <= sum_of_position_of_changes:
                                            index_2_to_skip = index_2_to_skip + 1
                                else:
                                    pattern_list.append(subsequence.words[index_2])
                                    index_list.append([index_2, index_2 + k])
                                    mdl_deviation_list.append(mdl_now)

                        sum_of_position_of_changes_old = sum_of_position_of_changes

            if len(pattern_list) > 1:
                if index_1 - word_1_index_before == 1 and len(pattern_list) >= word_1_len_candidate_list_before and len(pattern_list_all)>0:
                    if sum(mdl_deviation_list) < word_1_mdl_sum_before:
                        pattern_list_all[-1] = pattern_list
                        index_list_all[-1] = index_list
                        mdl_deviation_list_all[-1] = mdl_deviation_list
                else:
                    pattern_list_all.append(pattern_list)
                    index_list_all.append(index_list)
                    mdl_deviation_list_all.append(mdl_deviation_list)

                word_1_index_before = index_1
                word_1_mdl_sum_before = sum(mdl_deviation_list)
                word_1_len_candidate_list_before = len(pattern_list)

    return pattern_list_all, index_list_all, mdl_deviation_list_all