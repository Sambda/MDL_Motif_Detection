from search_strategies.search_whole_ts import get_motifs_for_whole_ts
import params as p


# Define k area for searching T
def get_area_k_flat_search(series, overjump):
    return list(range(int(series.len_sax/2), series.min_pattern_size_non_reduce, -overjump))


# Start Flat search
def start_flat_search(series):
    # init start and end point
    area_k = get_area_k_flat_search(series, p.steps_to_overjump)
    print("_________________________________\nFLAT SEARCH\n_________________________________")
    list_of_pattern, df_motifs = get_motifs_for_whole_ts(series, area_k)
    list_of_pattern = get_best_pattern(list_of_pattern)
    return list_of_pattern, df_motifs


# Create dict with best motifs for all possible different amounts of TSS per motif
def get_best_pattern(list_pattern):
    dict_best_motifs = {}
    for i in list_pattern:
        motif_size = list_pattern[i]['pattern_list_length']
        motif_dl = list_pattern[i]['mdl']
        if motif_size in dict_best_motifs:
            if motif_dl < dict_best_motifs[motif_size]['mdl']:
                dict_best_motifs[motif_size] = list_pattern[i]
                dict_best_motifs[motif_size]["k"] = i
        else:
            dict_best_motifs[motif_size] = list_pattern[i]
            dict_best_motifs[motif_size]["k"] = i

    return dict_best_motifs


