import time
from preprocessing.preprocess_data import read_data
import params as p
from search_strategies.hierachical_search import start_hierachical_search
from search_strategies.flat_search import start_flat_search
from utils.runtime_helper import get_min_possible_size
from objects.ts_object import set_series_object
from plot import plot_final_results, simple_plot, print_final_result
from search_strategies.second_motif_search_init import set_new_conditions


# Start Search
def start_search(strategy, series_original):
    if strategy == "hs":
        list_pattern = start_hierachical_search(series_original)

    elif strategy == "fs":
        list_pattern = start_flat_search(series_original)
    return list_pattern


# Start search_for_second_motif
def start_search_for_second_motif(indexes_of_pattern, series, number_of_reducing):
    # Calculate the Size und the breaks of the rest of the unused points in TS
    for key, value in indexes_of_pattern.items():
        ts, ts_norm, original_index, length_of_tss = set_new_conditions(value['indexes'], series.ts, series.ts_norm, number_of_reducing)

        series_search_2 = set_series_object(ts, ts_norm, series.data_number, series.alphabet_size, series.power_transformation, series.min_pattern_size_non_reduce, length_of_tss)
            # Search again in not used Areas
   #         list_of_pattern, series, indexes = first_search(number_of_reducing, series, Logger, series_original,
    #                                                        original_index)


   # if len(ts_norm) > series_original.min_pattern_size_non_reduce * 2 + 1:
  #      series = u.set_series_object(ts, ts_norm, data_number, alphabet_size, power, min_k, list_of_breaks)
  #      # Search again in not used Areas
  #      list_of_pattern, series, indexes = first_search(number_of_reducing, series, Logger, series_original,
  #                                                      original_index)


def run_main():
    time_start = time.time()
    ts_number = p.ts_number
    alphabet_size = p.alphabet_size

    ts, ts_norm, number_of_reducing = read_data(ts_number)

    # Init k area for original TS
    k_area = [2, int(len(ts) / 2)]
    min_k = get_min_possible_size(alphabet_size, len(ts_norm), k_area)

    # Set Original Series Object
    series_original = set_series_object(ts, ts_norm, ts_number, alphabet_size, min_k)

    # Plot reduced data
    # simple_plot(series_original.ts, "Original Data")
    # simple_plot(series_original.ts_norm, "Reduced Data")

    # Start first search
    list_of_pattern = start_search(p.kind_of_search, series_original)

    # Print final plot for first search
    print_final_result(list_of_pattern, series_original, number_of_reducing)

    #list_of_pattern_2 = start_search_for_second_motif(list_of_pattern, series_original, number_of_reducing)


    # Plot time
    time_end = time.time()
    print(round(((time_end - time_start)/60), 2),  " Minutes")


if __name__ == "__main__":
    run_main()

