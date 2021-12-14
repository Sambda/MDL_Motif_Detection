def set_new_conditions(indexes, ts, ts_norm, number_of_reducing, min_pattern_size_non_reduce = 8):

    ind = sum(indexes, [])
    index_list = []
    index_list.append(0)
    index_list.extend(ind)
    index_list.append(len(ts_norm))

    new_ind = []

    for i in range(0, len(index_list), 2):
        if index_list[i] != index_list[i + 1] and index_list[i + 1] - index_list[i] >= min_pattern_size_non_reduce:
            new_ind.append([index_list[i], index_list[i + 1]])

    new_ts = []
    new_ts_norm = []
    original_index = []
    length_of_tss = []
    for i in new_ind:
        w1 = i[0] * number_of_reducing
        w2 = i[1] * number_of_reducing-1
        new_ts.extend(ts[w1:w2])
        new_ts.extend('W')
        new_ts_norm.extend(ts_norm[i[0]:i[1]])
        new_ts_norm.extend('W')
        original_index.extend(list(range(i[0], i[1])))
        length_of_tss.append(len(new_ts_norm))

    #list_of_breaks = list_of_breaks[:-1]
    return new_ts, new_ts_norm, original_index, length_of_tss
    #return new_ind

