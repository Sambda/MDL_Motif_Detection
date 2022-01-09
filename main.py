import time
from preprocessing.get_data_runtime_tests import read_data
import params as p
from search_strategies.hierachical_search import start_hierarchical_search
from search_strategies.flat_search import start_flat_search
from utils.runtime_helper import get_min_possible_size, get_best_pattern
from objects.ts_object import set_series_object
from plot import simple_plot
from plot import print_final_result, create_path_for_plot_saving, print_final_result_per_level
from Logging.logger_setup import init_logger
from search_strategies.second_search import set_new_conditions
from plots.runtime_plots import plot_dict_values


# Start Search
def start_search(strategy, series_original, logger):
    level_dict = {}
    if strategy == "hs":
        list_pattern, df_motifs, level_dict = start_hierarchical_search(series_original, logger)

    elif strategy == "fs":
        list_pattern, df_motifs = start_flat_search(series_original)

    logger.set_text("Runtime whole TS:\n{}".format(df_motifs))
    return list_pattern, df_motifs, level_dict


def run_main():
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

    # Init Logger
    path = create_path_for_plot_saving(ts_number, series_original)
    logger = init_logger(series_original, path)
    print(path)

    # Plot reduced data
    simple_plot(series_original.ts, "Original Data")
    simple_plot(series_original.ts_norm, "Reduced Data")

    # Start first search
    list_of_pattern, df_motifs, level_dict = start_search(p.kind_of_search, series_original, logger)

    # Plot runtime images
    plot_dict_values(df_motifs, path)

    # Save df as CSV
    df_motifs.to_csv(str(path + "df_motifs.csv"), sep=',')

    # Log list
    logger.set_best_motifs(list_of_pattern)
    logger.set_text(str("Time complete: " + str(round(((time.time() - time_start)/60), 2)) + " minutes"))
    w = p.list_of_found_motifs_per_level

    if p.kind_of_search == "hs" and p.plot_levels == True:
        print_final_result_per_level(w, series_original, p.number_to_reduce, path, level_dict,w)
    # Print final plot for first search
    print_final_result(list_of_pattern, series_original, p.number_to_reduce, path, level_dict)

    best_indexes = get_best_pattern(list_of_pattern)
    ts, ts_norm, original_index, list_of_breaks = set_new_conditions(best_indexes, ts, ts_norm, p.number_to_reduce)
    # Set new Series Object

    if len(ts_norm) > series_original.min_pattern_size_non_reduce * 2 + 1:
        series = set_series_object(ts, ts_norm, ts_number, alphabet_size, min_k, list_of_breaks)
        # Search again in not used Areas
        list_of_pattern, series, indexes = start_search(p.kind_of_search, series, logger)
        print_final_result(list_of_pattern, series_original, p.number_to_reduce, path, level_dict)


if __name__ == "__main__":
    run_main()

