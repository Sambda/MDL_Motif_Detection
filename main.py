import time
from preprocessing.get_data_runtime_tests import read_data
import params as p
from search_strategies.hierachical_search import start_hierachical_search
from search_strategies.flat_search import start_flat_search
from utils.runtime_helper import get_min_possible_size
from objects.ts_object import set_series_object
from plot import plot_final_results, simple_plot
import os
from plot import print_final_result


# Start Search
def start_search(strategy, series_original):
    if strategy == "hs":
        list_pattern = start_hierachical_search(series_original)

    elif strategy == "fs":
        list_pattern = start_flat_search(series_original)
    return list_pattern


def run_main(data_name):
    time_start = time.time()
    ts_number = p.ts_number
    alphabet_size = p.alphabet_size

    ts, ts_norm = read_data(ts_number)
    print("LEN:", len(ts), len(ts_norm))
    print("number_to_reduce:", p.number_to_reduce)

    # Init k area for original TS
    k_area = [2, int(len(ts) / 2)]
    min_k = get_min_possible_size(alphabet_size, len(ts_norm), k_area)

    # Set Original Series Object
    series_original = set_series_object(ts, ts_norm, ts_number, alphabet_size, min_k)

    # Plot reduced data
    simple_plot(series_original.ts, "Original Data")
    simple_plot(series_original.ts_norm, "Reduced Data")

    # Start first search
    list_of_pattern = start_search(p.kind_of_search, series_original)

    time_end = time.time()
    print(round(((time_end - time_start)/60), 2),  " Minutes")

    # Print final plot for first search
    print_final_result(list_of_pattern, series_original, p.number_to_reduce, data_name)


if __name__ == "__main__":
    run_main("ecg")

