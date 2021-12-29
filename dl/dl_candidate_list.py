import numpy as np
import dl.dl_helper as dl_helper
import params as p


def mdl_for_candidate_list(subsequence, series):
    k = subsequence.k
    candidate_list_tss_all, candidate_list_indexes_all, candidate_list_dl_dev_all = [], [], []

    # Bad encoding for compairing with MDL
    dl_sax = dl_helper.log_2(subsequence.k, series.alphabet_size)

    # Location of pattern
    dl_dev_4 = dl_helper.log_2(1, series.len_sax)

    # Mdl cost if difference is 0
    mdl_for_zero_difference = 1.51

    # If a word already is in candidate list with dist 0 to target word not necessary to look at it again, skip it.
    indexes_to_skip = []

    tgs_index_before = 0
    word_1_mdl_sum_before = np.inf
    word_1_len_candidate_list_before = 0

    sum_of_position_of_changes_old = np.inf
    index_2_to_skip = 0

    for index_1, word_1 in enumerate(subsequence.words[:-1]):
        candidate_list_tss = []
        if index_1 not in indexes_to_skip:
            if "W" not in subsequence.words_numeric[index_1]:
                # Add target candidate to list
                candidate_list_tss = [word_1]
                candidate_list_indexes = [[index_1, index_1 + k]]
                candidate_list_dl_dev = [mdl_for_zero_difference]

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
                            sum_of_position_of_changes = k - difference_array.count(0)
                            # Only got further if sum of position changes is under threshold
                            # TODO threshold
                            #if sum_of_position_of_changes <= series.dict_threshold[k]:

                            if sum_of_position_of_changes == 0:
                                indexes_to_skip.append(index_2)
                                dl_dev = mdl_for_zero_difference
                            else:
                                dl_dev = dl_helper.calc_mdl_for_distance_array(sum_of_position_of_changes, k, difference_array)

                            if dl_dev + dl_dev_4 < dl_sax:

                                if index_2 - candidate_list_indexes[-1][0] == 1:
                                    if dl_dev >= candidate_list_dl_dev[-1]:
                                        pass
                                    else:
                                        # TODO: evaluate difference candidate list
                                        # Delete old candidate
                                        candidate_list_tss = candidate_list_tss[:-1]
                                        candidate_list_indexes = candidate_list_indexes[:-1]
                                        candidate_list_dl_dev = candidate_list_dl_dev[:-1]
                                        # Add new candidate
                                        candidate_list_tss.append(subsequence.words[index_2])
                                        candidate_list_indexes.append([index_2, index_2 + k])
                                        candidate_list_dl_dev.append(dl_dev)

                                        if sum_of_position_of_changes_old <= sum_of_position_of_changes:
                                            index_2_to_skip = index_2_to_skip + 1
                                else:
                                    candidate_list_tss.append(subsequence.words[index_2])
                                    candidate_list_indexes.append([index_2, index_2 + k])
                                    candidate_list_dl_dev.append(dl_dev)

                        sum_of_position_of_changes_old = sum_of_position_of_changes

            if len(candidate_list_tss) > 1:
                if index_1 - tgs_index_before == 1 and len(candidate_list_tss) >= word_1_len_candidate_list_before and len(
                        candidate_list_tss_all) > 0:
                    if sum(candidate_list_dl_dev) < word_1_mdl_sum_before:
                        candidate_list_tss_all[-1] = candidate_list_tss
                        candidate_list_indexes_all[-1] = candidate_list_indexes
                        candidate_list_dl_dev_all[-1] = candidate_list_dl_dev
                else:
                    candidate_list_tss_all.append(candidate_list_tss)
                    candidate_list_indexes_all.append(candidate_list_indexes)
                    candidate_list_dl_dev_all.append(candidate_list_dl_dev)

                tgs_index_before = index_1
                word_1_mdl_sum_before = sum(candidate_list_dl_dev)
                word_1_len_candidate_list_before = len(candidate_list_tss)

    return candidate_list_tss_all, candidate_list_indexes_all, candidate_list_dl_dev_all
