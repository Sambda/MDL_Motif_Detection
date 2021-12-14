import search_strategies.second_motif_search_init as search_helper
from dl.dl_candidate_list import mdl_for_candidate_list
from objects.tss_object import set_subsequence_object
from overlappings.overlapping_remover import remove_overlapping
from objects.motif_object import Motifs
import numpy as np
from dl.dl_ts import calculate_mdl_for_ts
import time
from plot import run_time_plot


# calculate MDL encoding for motifs, sorted by cheapness per amount of motifs per cluster
def calculate_mdl_for_motifs(motifs, series):
    # dict for best results per candidate_list_length
    d = dict()
    min_mdl = np.inf
    for i, pattern_list in enumerate(motifs.candidates):
        len_pattern = motifs.k_list[i]
        pattern_list_len = len(pattern_list)
        mdl = calculate_mdl_for_ts(motifs.mdl_dev[i], pattern_list_len, len_pattern, series.len_sax,
                                     series.alphabet_size, True)

        if mdl < series.worst_case:
            if min_mdl >= mdl:
                min_mdl = mdl
                d = {"pattern_list": pattern_list,
                     "mdl": mdl, "indexes": motifs.indexes[i],
                     "pattern_list_length": pattern_list_len}
    return d


def get_motifs_for_whole_ts(series, search_area_all):
    print("\n_________________________________"
          "\nStart search:\n"
          "\n_________________________________")
    motifs = Motifs()
    list_best_pattern_for_k = {}
    runtime_x = []
    runtime_y = []
    amount_of_symbols = []
    for k in search_area_all:
        time_start_k = time.time()

        # reset Motif for new k
        motifs.reset()

        # Set sequence Object
        seq = set_subsequence_object(k, series)

        # Collect all possible motif candidates
        pattern_list_all, index_list_all, mdl_deviation_list_all = mdl_for_candidate_list(seq, series)

        sum = 0
        for i in pattern_list_all:
            sum += sum + len(i)
        print("for k = {} length of found possibilities is {} with {} subsequences".format(k, len(pattern_list_all), (sum*k)/100))

        # Collect all possible pattern (non-overlapping) for different k's
        motifs = remove_overlapping(pattern_list_all, index_list_all, mdl_deviation_list_all, seq, motifs)

        dict_best_pattern_for_k = calculate_mdl_for_motifs(motifs, series)
        if len(dict_best_pattern_for_k) > 0:
            list_best_pattern_for_k[k] = dict_best_pattern_for_k
            list_best_pattern_for_k[k]["k"] = k

        time_end_k = time.time()
        time_sum_k = round(((time_end_k - time_start_k) / 60), 4)
        runtime_x.append(k)
        runtime_y.append(time_sum_k)
        amount_of_symbols.append((sum*k)/100)

    run_time_plot(runtime_x, runtime_y, title="Runtime")
    run_time_plot(runtime_x[:-1], amount_of_symbols[:-1], title="Amount")

    return list_best_pattern_for_k
