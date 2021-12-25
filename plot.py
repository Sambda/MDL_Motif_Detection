import matplotlib.pyplot as plt
import utils as u
import params as p
from matplotlib.gridspec import GridSpec
import os


def simple_plot(ts, title="", x_label='', y_label = ''):
    plt.figure(figsize=(15, 4))
    plt.plot(list(range(len(ts))), ts)
    plt.title(title) #Vehicle Miles Traveled (FHWA):
    plt.ylabel(y_label, fontsize=12)
    plt.xlabel(x_label, fontsize=12)
    plt.show()


# plot the smoothed timeseries with intervals
def plot_smoothed_data(ts, ts_smoothed, low, up):
    plt.figure(figsize=(18, 5))

    plt.plot(ts, color='yellow', alpha=0.9, linewidth=1)
    plt.plot(ts_smoothed, linewidth=1, color='blue')

    plt.title("Smoothed Timeseries")

    plt.fill_between(range(len(ts_smoothed)), low[0], up[0], alpha=0.5)
    plt.show()


def show_plot_with_quantils(ts, sax, quantils):
    plt.figure(figsize=(14, 8))
    for i in quantils:
        if i == int or float:
            plt.axhline(y=i, xmin=0.0, xmax=1.0, color='lightgrey', linewidth=2.5)

    plt.plot(ts, ms=4, linewidth=0.5)

    plt.title("SAX Breakpoints")

    for x, y, s in zip(range(len(ts)), ts, sax):
        plt.text(x, y, s, ha='center', va="bottom", fontsize=14, color='#ff7f0e')

    plt.show()


def plot_time_for_candidate_search(time_difference):
    plt.plot(time_difference.k_list, time_difference.time_list_complete, color="blue", label='Complete')
    plt.plot(time_difference.k_list, time_difference.time_list_pulp, color="red", label='Pulp')
    plt.gca().invert_xaxis()
    plt.title(sum(time_difference.time_list_complete))
    plt.show()


def show_plot_bins(ts, ts_sax, cuts, title):
    plt.figure(figsize=(32, 8))
    for i in cuts:
        if i == int or float:
            plt.axhline(y=i, xmin=0.0, xmax=1.0, color='lightgrey',linewidth=2.5)

    plt.plot(ts, ms=4, label='Normalised', linewidth=0.5)

    for x, y, s in zip(range(len(ts)), ts, ts_sax):
        plt.text(x, y, s, ha='center', va="bottom", fontsize=14, color='#ff7f0e')
    plt.xlabel('Time', fontsize=12)
    plt.title('SAX ' + str(title), fontsize=16)
    plt.show()


# Plot for coloring detected motifs
def show_plt(index_list_sum, ts_original, pattern, title, save, path, k):
    color_list = ["#FF0000", "#F67332"]
    x = list(range(0, len(ts_original[:-1])))

    fig, ax = plt.subplots(figsize=(8, 4))
    plt.plot(x, ts_original[:-1], "#717170")

    index_list = [(list(range(sub_list[0], sub_list[1]))) for sub_list in index_list_sum]
    for x1, x2, y1, y2 in zip(x, x[1:], ts_original, ts_original[1:]):

        for color_tmp, ind in enumerate(index_list):
            if x1 in ind:
                if color_tmp % 2:
                    color = color_list[0]
                else:
                    color = color_list[1]
                plt.plot([x1, x2], [y1, y2], color)

    ax.set_xlabel("{} different pattern with length: {} where found. \nParams: alphabet_size: {}, smooth: {}, differencing: {}, power: {}, z-norm: {}"
                  .format(len(pattern), k, p.alphabet_size, p.smooth_fraction, p.differencing, p.power_transformation, p.z_norm))
    plt.title(title)
    if save:
        path = path + str(k)
        plt.savefig(path, dpi=400, bbox_inches='tight')
    plt.show()


def get_title(d, series, data_name, indexes_len):
    dl_ts = round(d['mdl'], 2)
    dl_sax = round(series.worst_case, 2)
    percent = str(round(dl_ts/dl_sax, 2))
    title = str(data_name) + "\nMDL: " + str(dl_ts) + " DL: " + str(dl_sax) + " Savings in pertentage: " + percent
    x_axis = "{} different pattern with length: {} where found. \nParams: alphabet_size: {}, smooth: {}, differencing: {}, power: {}, z-norm: {}"\
        .format(indexes_len, d['k'], p.alphabet_size, p.smooth_fraction, p.differencing, p.power_transformation, p.z_norm)
    return title, x_axis


def create_path_for_plot_saving(data_name, series):
    path = "images/" + str(data_name) + "/"
    path = path + str(len(series.ts)) \
           + "/" + str(series.len_sax) \
           + "/" + str(series.alphabet_size) + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    return path


# Plot results
def print_final_result(list_of_pattern, series, number_of_reducing, data_name):
    path = create_path_for_plot_saving(data_name, series)
    for i, d in enumerate(list_of_pattern):
        pattern = list_of_pattern[d]
        indexes = [[i[0] * number_of_reducing, i[1] * number_of_reducing] for i in
                   pattern['indexes']] if number_of_reducing else pattern['indexes']
        title, x_axis_text = get_title(pattern, series, data_name, len(indexes))
        color_list = ["#FF0000", "#F67332"]
        x = list(range(0, len(series.ts[:-1])))

        fig, ax = plt.subplots(figsize=(8, 4))
        plt.plot(x, series.ts[:-1], "#717170")

        index_list = [(list(range(sub_list[0], sub_list[1]))) for sub_list in indexes]
        for x1, x2, y1, y2 in zip(x, x[1:], series.ts, series.ts[1:]):

            for color_tmp, ind in enumerate(index_list):
                if x1 in ind:
                    if color_tmp % 2:
                        color = color_list[0]
                    else:
                        color = color_list[1]
                    plt.plot([x1, x2], [y1, y2], color)

        ax.set_xlabel(x_axis_text)
        plt.title(title)
        if p.save:
            path = path + str(pattern['k'])
            plt.savefig(path, dpi=400, bbox_inches='tight')
        plt.show()


def plot_final_results(d, series, number_of_reducing, path, data_name, save):

    indexes = [[i[0] * number_of_reducing, i[1] * number_of_reducing] for i in
               d['indexes']] if number_of_reducing else d['indexes']
    title, x_axis_text = get_title(d, series, data_name, len(indexes))
    color_list = ["#FF0000", "#F67332"]
    x = list(range(0, len(series.ts[:-1])))

    fig, ax = plt.subplots(figsize=(8, 4))
    plt.plot(x, series.ts[:-1], "#717170")

    index_list = [(list(range(sub_list[0], sub_list[1]))) for sub_list in indexes]
    for x1, x2, y1, y2 in zip(x, x[1:], series.ts, series.ts[1:]):

        for color_tmp, ind in enumerate(index_list):
            if x1 in ind:
                if color_tmp % 2:
                    color = color_list[0]
                else:
                    color = color_list[1]
                plt.plot([x1, x2], [y1, y2], color)

    ax.set_xlabel(x_axis_text)
    plt.title(title)
    if save:
        path = path + str(d['k'])
        plt.savefig(path, dpi=400, bbox_inches='tight')
    plt.show()


def hist_plot(x, y):
    fig = plt.figure()
    gs = GridSpec(4, 10)

    ax_scatter = fig.add_subplot(gs[0:4, 0:8])
    ax_hist_y = fig.add_subplot(gs[0:4, 8:10])

    ax_scatter.plot(x, y)

    ax_hist_y.hist(y, orientation='horizontal')

    plt.show()


def run_time_plot(x, y, y2=[], y3=[], title = ""):
    plt.figure(figsize=(10, 4))
    plt.plot(x, y)
    # plt.plot(x, y2)
    # plt.plot(x, y3)
    plt.gca().invert_xaxis()
    plt.title("Runtime ")
    plt.show()
