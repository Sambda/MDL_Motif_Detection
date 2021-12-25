import dl.dl_helper as h
from dl.dl_ts import calculate_mdl_for_ts


# Calculate die minimal motif length for which it could be rentable
def get_min_possible_size(alphabet_size, len_ts, k_area, mdl_deviation=1.51):
    dl = h.log_2(len_ts, alphabet_size)
    for k in list(range(k_area[0], k_area[1])):
        max_possible_tss = int(len_ts/k)
        mdl_deviation_list = [mdl_deviation] * max_possible_tss
        mdl = calculate_mdl_for_ts(mdl_deviation_list, max_possible_tss, k, len_ts, alphabet_size)
        if dl > mdl:
            return k