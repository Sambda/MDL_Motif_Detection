import matplotlib.pyplot as plt
import params as p
from matplotlib.gridspec import GridSpec
import os
import collections


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


def get_title(d, series, indexes_len, number_of_reducing, level):
    dl_ts = round(d['mdl'], 2)
    dl_sax = round(series.worst_case, 2)
    percent = round((dl_ts/dl_sax)*100, 1)
    title = r"$\bf{ Level(s) " + str(level) + "}$" + "\n" +str(p.data_name) + "\nDL_TS: " + str(dl_ts) + "\nDL_SAX: " + str(dl_sax) + " | Compression to " + str(percent) + "%"
  #  x_axis = "Motif with {} subsequences of length {}.\nAlphabet_size: {}, Smooth: {}, Differencing: {}, \nPower Transformation: {}, Z-normalisation: {}"\
   #     .format(indexes_len, d['k'], p.alphabet_size, p.smooth_fraction, p.differencing, p.power_transformation, p.z_norm)
    x_axis = "Motif of length {} points, consisting {} subsequences.".format(d['k']*number_of_reducing, indexes_len)
    return title, x_axis, round(percent/series.alphabet_size,2)


def create_path_for_plot_saving(data_name, series):
    path = "images/" + str(data_name) + "/"
    path = path + str(p.kind_of_search) \
        + "/" + str(len(series.ts)) \
        + "/" + str(series.len_sax) \
        + "/" + str(series.alphabet_size) \
        + "/" + str(p.differencing) \
        + "/" + str(p.power_transformation) + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    return path


# Plot results
def print_final_result(list_of_pattern, series, number_of_reducing, path, level_dict_all):
    for i, d in enumerate(list_of_pattern):
        pattern = list_of_pattern[d]
        indexes = [[i[0] * number_of_reducing, i[1] * number_of_reducing] for i in
                   pattern['indexes']] if number_of_reducing else pattern['indexes']

        m = [k for k, v in level_dict_all.items() if float(v) == d]
        title, x_axis_text, percent = get_title(pattern, series, len(indexes), number_of_reducing, m)
        color_list = ["#f6a832", "#F67332"]
        x = list(range(0, len(series.ts[:-1])))

        fig, ax = plt.subplots(figsize=(10, 5))
        plt.plot(x, series.ts[:-1], "#717170")

        index_list = [(list(range(sub_list[0], sub_list[1]))) for sub_list in indexes]
        for x1, x2, y1, y2 in zip(x, x[1:], series.ts, series.ts[1:]):

            for color_tmp, ind in enumerate(index_list):
                if x1 in ind:
                    if color_tmp % 2:
                        color = color_list[0]
                    else:
                        color = color_list[1]
                    plt.plot([x1, x2], [y1, y2], color,  linewidth=2)
        title_axis = p.x_axis + "\n" + x_axis_text
        ax.set_xlabel(title_axis, fontsize=15)
        ax.set_ylabel(p.y_axis, fontsize=15)
        plt.title(title, fontsize=16)

        if p.save:
            path_plot = path + str(percent) + ".png"
            plt.savefig(path_plot, dpi=400, bbox_inches='tight')
        plt.show()


def print_final_result_per_level(list_of_pattern, series, number_of_reducing, path, level_dict_all,w):
    level_dict_all = {y: x for x, y in level_dict_all.items()}
    for ind,pattern in enumerate(list_of_pattern):
        indexes = [[i[0] * number_of_reducing, i[1] * number_of_reducing] for i in
                   pattern[0:2]] if number_of_reducing else pattern[0:2]

        title = str("Level: {}".format(level_dict_all[pattern[2]], pattern[4], pattern[3]))
        x_axis_text, percent = "",""
        x_axis_text = indexes

        color_list = ["#f6a832", "#F67332"]
        x = list(range(0, len(series.ts[:-1])))

        fig, ax = plt.subplots(figsize=(10, 5))
        plt.plot(x, series.ts[:-1], "#717170")

        index_list = [(list(range(sub_list[0], sub_list[1]))) for sub_list in indexes]
        for x1, x2, y1, y2 in zip(x, x[1:], series.ts, series.ts[1:]):

            for color_tmp, ind in enumerate(index_list):
                if x1 in ind:
                    if color_tmp % 2:
                        color = color_list[0]
                    else:
                        color = color_list[1]
                    plt.plot([x1, x2], [y1, y2], color,  linewidth=2)
        title_axis = p.x_axis + "\n" + str(x_axis_text)
        ax.set_xlabel(title_axis, fontsize=15)
        ax.set_ylabel(p.y_axis, fontsize=15)
        plt.title(title, fontsize=16)

        if p.save:
            path_plot = path + str(percent) + ".png"
            plt.savefig(path_plot, dpi=400, bbox_inches='tight')
        plt.show()

def hist_plot(x, y):
    fig = plt.figure()
    gs = GridSpec(4, 10)

    ax_scatter = fig.add_subplot(gs[0:4, 0:8])
    ax_hist_y = fig.add_subplot(gs[0:4, 8:10])

    ax_scatter.plot(x, y)

    ax_hist_y.hist(y, orientation='horizontal')

    plt.show()


def run_time_plot(x, y, y2=[], y3=[], title=""):
    plt.figure(figsize=(10, 4))
    plt.plot(x, y)
    # plt.plot(x, y2)
    # plt.plot(x, y3)
    plt.gca().invert_xaxis()
    plt.title("Runtime ")
    plt.show()


def plot_runtime_dict(x, y, title, path):
    plt.title(title)
    plt.plot(x, y, "k.")
    if p.save:
        path = path + title
        plt.savefig(path, dpi=400, bbox_inches='tight')


def runtime_comparision_plot(df_list):
    title_list = ["ecg", "ecg5D", "olive", "coffee"]
    for i, t in zip(df_list, title_list):
        plt.plot(list(range(len(i["runtime"]))), i["runtime"], label=t)
    plt.title("Runtime")
    plt.legend(loc="upper right")
    plt.xlabel('k', fontsize=10)
    plt.ylabel('runtime in seconds', fontsize=10)
    plt.gca().invert_xaxis()
    plt.show