import numpy as np
import dl.dl_helper as dl_helper
import params as p
from dl.dl_ts import calculate_mdl_for_ts
import objects.ts_object as ts_obj
import search_strategies.search_helper as search_helper
from search_strategies.search_whole_ts import get_motifs_for_whole_ts
import time
from plot import plot_final_results, run_time_plot


# Get search Area for hierachical search
def get_area_k_hs(len_sax_tmp):
    return [int(len_sax_tmp/3 + 1), int(len_sax_tmp/ 2)]


# Start Search for the best k's in the whole series
def get_area_k_secound_search(list_of_ks):
    search_areas_all = []

    # Combine list of all collected k's and delete repetitions
    list_of_ks = list(np.unique(sum(list_of_ks, [])))

    if p.search_again_for_best_ks:

        # Search in whole area for all collected k's
        for k in list_of_ks:
            # define range to search in the neighborhood again
            # TODO better way for percentage_skip
            range_to_overjump = 0

            # Define Search Area k = 50 -> Area = [48, 50, 52]
            search_area = list(range(k - range_to_overjump - 1, k + range_to_overjump))
            print("Search_area: ", search_area)
            search_area = [i for i in search_area if i > 8]
            search_areas_all.append(search_area)

    return search_areas_all


def start_search(series, area_list):
    # Move pattern search always two percent further.
    # TODO better way for percentage_skip
    percentage_skip = int(series.len_sax/100)
    range_to_skip = percentage_skip if percentage_skip > 1 else 1

    # Get best Motifs in range of k
    dict_best_motif = get_the_best_k(series, area_list[0], area_list[1], range_to_skip)
    # Search again around the best k
    # If the highest possible k was best/maybe because no pattern was found skip this step
    if p.search_again_in_neighborhood and "k" in dict_best_motif and dict_best_motif['k'] != area_list[1] and range_to_skip != 1:
        print("------")
        range_to_skip = range_to_skip if range_to_skip > 1 else 2
        start, end = dict_best_motif["k"] - range_to_skip+1, dict_best_motif["k"] + range_to_skip
        start = area_list[0] if start <= area_list[0] else start
        end = area_list[1] if end >= area_list[1] else end
        dict_best_motif = get_the_best_k(series, start, end)
    return dict_best_motif


def get_the_best_k(series, start, end, range_to_search="1"):

    dict_best_pattern_all = {"mdl": np.inf}
    for k in range(start, end, range_to_search):
        print("k:", k)

        time_start_k = time.time()

        words = search_helper.create_word_lists(series.sax, k)
        words_numeric = search_helper.create_word_lists(series.sax_numeric, k)
        words_numeric_2 = search_helper.create_word_lists(series.sax_numeric_2, k) if series.double else []

        dict_best_pattern = {"mdl": series.worst_case, "pattern_1": [""],
                             "pattern_2": [""], "k": int(series.len_sax / 2),
                             "index_1": [0, int(series.len_sax / 2)],
                             "index_2": [int(series.len_sax / 2), series.len_sax],
                             "worst_case": series.worst_case}

        # Runtime Plot
        # time_after_words_creation = time.time()
        # time_sum_k = round(((time_after_words_creation - time_start_k) / 60), 4)
        # runtime_y_middle.append(time_sum_k)

        # Mdl cost if difference is 0
        mdl_for_zero_difference = 1.51

        exp_way = dl_helper.log_2(k, series.alphabet_size)

        for index_1, word_1 in enumerate(words[:-1]):
            if "W" not in word_1:
                start_index_words_2 = index_1 + k

                for index_2, word_2 in enumerate(words[start_index_words_2:]):
                    if "W" not in word_2:
                        index_2 = index_2 + start_index_words_2

                        # Sum of difference between word_1 and word_2
                        difference_array = dl_helper.get_difference_array_double(words_numeric[index_1],
                                                                                 words_numeric_2[index_1],
                                                                                 words_numeric[index_2],
                                                                                 words_numeric_2[index_2])

                        # On how many positions something have to be changed
                        sum_of_position_of_changes = k - difference_array.count(0)

                        if sum_of_position_of_changes == 0:
                            mdl_deviation = mdl_for_zero_difference
                        else:
                            mdl_deviation = dl_helper.calc_mdl_for_distance_array(sum_of_position_of_changes, k,
                                                                        difference_array)

                        mdl = calculate_mdl_for_ts([mdl_deviation], 2, k, series.len_sax, series.alphabet_size)

                        if dict_best_pattern["mdl"] > mdl and mdl < series.worst_case:
                            # dict_best_pattern["mdl"] = mdl
                            dict_best_pattern["mdl"] = mdl_deviation
                            dict_best_pattern["pattern_1"] = [word_1]
                            dict_best_pattern["pattern_2"] = [word_2]
                            dict_best_pattern["k"] = k
                            dict_best_pattern["index_1"] = [index_1, index_1 + k]
                            dict_best_pattern["index_2"] = [index_2, index_2 + k]
                            dict_best_pattern["worst_case"] = series.worst_case

        # Runtine plot
        # time_end_k = time.time()
        # time_sum_k = round(((time_end_k - time_start_k) / 60), 4)
        # runtime_x.append(k)
        # runtime_y.append(time_sum_k)

        if dict_best_pattern["mdl"] < dict_best_pattern_all['mdl']:
            dict_best_pattern_all = dict_best_pattern

    # run_time_plot(runtime_x, runtime_y, runtime_y_middle)
    return dict_best_pattern_all


# Start pattern search in subsequences of the ts
def start_pattern_search_smaller_series(series, dict_tree, level):
    list_of_dicts_per_level = []
    list_of_ks = []
    index_list = ["index_1", "index_2"]

    # Run new search in the sub areas of the two before founden subsequences
    for i in index_list:
        # define new series object of the subsequence
        series_sub = ts_obj.set_new_series(series, dict_tree[i], dict_tree["k"])
        # define the searching area
        area_k = get_area_k_hs(series_sub.len_sax)
        print("\n_________________________________\nLEVEL {}.{}\n_________________________________".format(level, i[-1]))
        print("New Series Length: {}\nSearch Area: {}\n".format(series_sub.len_sax, area_k))

        # Start searching best k
        dict_best_motifs = start_search(series_sub, area_k)

        dict_best_motifs["index_1"] = [dict_best_motifs["index_1"][0] + dict_tree[i][0], dict_best_motifs["index_1"][1] + dict_tree[i][0]]
        dict_best_motifs["index_2"] = [dict_best_motifs["index_2"][0] + dict_tree[i][0], dict_best_motifs["index_2"][1] + dict_tree[i][0]]
        list_of_dicts_per_level.append(dict_best_motifs)
        list_of_ks.append(dict_best_motifs['k'])
    return list_of_dicts_per_level, list_of_ks


def start_hierachical_search(series_original, logger):

    list_of_ks = []

    # init start and end point
    area_k = get_area_k_hs(series_original.len_sax)
    level = 1
    print("_________________________________\nLEVEL " + str(level) + "\n_________________________________")
    print("Series Length: {} \nSearch Area: {}\n".format(series_original.len_sax, area_k))

    # Init Search based on whole TS
    dict_tree = start_search(series_original, area_k)
    list_of_ks.append([dict_tree['k']])

    while dict_tree["k"] > series_original.min_pattern_size_non_reduce * 2 + 1:
        level += 1
        dict_list, list_ks = start_pattern_search_smaller_series(series_original, dict_tree, level)

        list_of_ks.append(list_ks)

        # Take Motifs with lower MDL for the next search
        dict_tree = dict_list[0] if dict_list[0]["mdl"] <= dict_list[1]["mdl"] else dict_list[1]
    search_area = get_area_k_secound_search(list_of_ks)
    logger.set_text("\nList of k's: {}".format(list_of_ks))
    logger.set_text("SEARCH AREA: {}\n".format(search_area))

    # Restart search for spezifiy k's in whole ts
    list_of_pattern = get_motifs_for_whole_ts(series_original, list(np.unique(sum(search_area, []))))

    return list_of_pattern

