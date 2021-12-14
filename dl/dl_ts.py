import dl.dl_helper as h


# Wie viele Änderungen log*(Anzahl_der_Positionen_der_Änderungen) +
# Wo sind die Änderungen? Anzahl_der_Positionen_der_Änderungen * log2(länge_segment) +
# log*(kosten Änderungen Stelle 1)+ 1(Indikatorbit +/-) + ... + log*(kosten Änderungen Stelle n)+ 1(Indikatorbit +/-)
# encode costs of a spezific change at a position + 1 as indicatorbit for saying if + or -
def calculate_mdl_for_ts(mdl_deviation, len_pattern_list, len_pattern, len_sax, a_size,
                         logs=False):
    # Length of segments
    len_segments = h.log_star(len_pattern)
    # Frequency of segments
    freq_segments = h.log_star(len_pattern_list)
    # Structure of first segment
    structure_segment = h.log_2(len_pattern, a_size)
    # Start index of segment
    start_indexes = h.log_2(len_pattern_list, len_sax-len_pattern)
    # Indicator bits if Segments are different
    indicator_bits = len_pattern_list
    # MDL sum of the deviation of the motifs to the original one
    mdl_difference = sum(mdl_deviation)
    # Encoding for sax components not in pattern
    not_in_pattern = h.log_2((len_sax - len_pattern * len_pattern_list), a_size)
    # print("sum(mdl_difference_all)", sum(mdl_difference_all))
    mdl = len_segments + freq_segments + structure_segment + start_indexes + indicator_bits + mdl_difference + not_in_pattern

    return mdl
