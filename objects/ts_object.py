import string
from datetime import datetime
from dl.dl_helper import log_2
import re
import params as p
from preprocessing.sax import apply_sax
import copy
import numpy as np

# Define class
class Series(object):
    def __init__(self, ts: list, ts_norm: list, double: int, data_number: int, alphabet_size: int,
                 min_possible_pattern_size: int, time,
                 sax: list = [], sax_2: list = [], sax_numeric: list = [], sax_numeric_2: list = [],
                 candidate_list: list = [], mdl_deviation_lists: list = [], index_lists: list = [],
                 ):
        self.ts = ts
        self.ts_norm = ts_norm
        self.double = double
        self.sax = sax
        self.len_sax = len(sax)
        self.sax_2 = sax_2
        self.data_number = data_number
        self.alphabet_size = alphabet_size
        self.alphabet_list = list(string.ascii_lowercase)[0:alphabet_size]
        self.min_pattern_size_non_reduce = min_possible_pattern_size
        self.time = time
        self.power_transformation = p.power_transformation
        self.sax_numeric = sax_numeric
        self.sax_numeric_2 = sax_numeric_2
        self.candidate_list = candidate_list
        self.mdl_deviation_lists = mdl_deviation_lists
        self.index_lists = index_lists


# abcdaa -> 123411
def create_number_series(string, list_alphabet):
    for i, j in enumerate(list_alphabet):
        i += 1
        string = re.sub(str(j), str(i), string)
    string = np.array(list(map(int, string)))
    return string


def set_new_series(series, index, area_length):
    series_s = copy.deepcopy(series)
    series_s.sax = series.sax[index[0]:index[1]]
    series_s.sax_2 = series.sax_2[index[0]:index[1]]
    series_s.sax_numeric = series.sax_numeric[index[0]:index[1]]
    series_s.sax_numeric_2 = series.sax_numeric_2[index[0]:index[1]]
    series_s.ts = series.ts[index[0]:index[1]]
    series_s.ts_norm = series.ts_norm[index[0]:index[1]]
    series_s.len_sax = area_length
    series_s.worst_case = log_2(area_length, series.alphabet_size)
    return series_s


def set_series_object(ts, ts_norm, data_number, alphabet_size, min_possible_pattern_size, list_of_breaks=[]):
    time = datetime.now().strftime('%d%m%H%M%S')
    series = Series(ts, ts_norm, p.double_sax, data_number, alphabet_size,min_possible_pattern_size, time)
    series = apply_sax(series)
    series.worst_case = log_2(series.len_sax, series.alphabet_size)
    series.sax_numeric = create_number_series("".join(series.sax), series.alphabet_list)
    series.sax_numeric_2 = create_number_series("".join(series.sax_2), series.alphabet_list) if series.double else ""

    if list_of_breaks != []:
        sax_num = list(series.sax_numeric)
        sax_num2 = list(series.sax_numeric_2)
        sax = list(series.sax)
        for i in list_of_breaks:
            sax_num[i] = "W"
            sax_num2[i] = "W"
            sax[i] = "W"
        series.sax_numeric = "".join(sax_num)
        series.sax_numeric2 = "".join(sax_num2)
        series.sax = "".join(sax)
    return series
