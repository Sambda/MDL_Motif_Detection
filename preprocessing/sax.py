import numpy as np
from saxpy.sax import ts_to_string
import params as p
from saxpy.alphabet import cuts_for_asize
import pandas as pd
from plot import show_plot_with_quantils, simple_plot


def get_sax_2(series, breakpoint_list):

    breakpoints_2 = []
    breakpoints_alphabet_2 = []
    breakpoints_2.append(breakpoint_list[0] - 0.0001)
    breakpoints_alphabet_2.append(series.alphabet_list[0])

    if p.three_double_sax:

        var = p.threshold_double
        for i in range(len(breakpoint_list) - 2):
            i = i + 1
            diff1 = breakpoint_list[i] - breakpoint_list[i - 1]
            diff2 = breakpoint_list[i + 1] - breakpoint_list[i]
            breakpoints_2.append(breakpoint_list[i] - diff1 / var)
            breakpoints_2.append(breakpoint_list[i])
            breakpoints_2.append(breakpoint_list[i] + diff2 / var)
            breakpoints_alphabet_2.append(series.alphabet_list[i])
            breakpoints_alphabet_2.append(series.alphabet_list[i - 1])
            breakpoints_alphabet_2.append(series.alphabet_list[i])

        breakpoints_2.append(breakpoint_list[-1] + (breakpoint_list[-2] - breakpoint_list[-1]) / var)
        breakpoints_2.append(breakpoint_list[-1])
        breakpoints_2.append(breakpoint_list[-1] + (max(series.ts_norm) - breakpoint_list[-1]) / var)
        breakpoints_2.append(max(series.ts_norm) + 0.01)
        breakpoints_alphabet_2.append(series.alphabet_list[-1])
        breakpoints_alphabet_2.append(series.alphabet_list[-2])
        breakpoints_alphabet_2.append(series.alphabet_list[-1])
    else:
        for i in range(len(breakpoint_list) - 1):
            i = i + 1
            middle = (breakpoint_list[i] + breakpoint_list[i - 1]) / 2
            breakpoints_2.append(middle)
            breakpoints_2.append(breakpoint_list[i])
            breakpoints_alphabet_2.append(series.alphabet_list[i])
            breakpoints_alphabet_2.append(series.alphabet_list[i - 1])

        breakpoints_2.append((max(series.ts_norm) + breakpoint_list[-1]) / 2)
        breakpoints_2.append(max(series.ts_norm) + 0.01)
        breakpoints_alphabet_2.append(series.alphabet_list[-1])

    breakpoints_2 = np.around(breakpoints_2, decimals=5)
    df = pd.DataFrame(series.ts_norm)
    c = pd.cut(
        df.stack(),
        breakpoints_2,
        labels=breakpoints_alphabet_2,
        ordered=False
    )
    df = df.join(c.unstack().add_suffix('_sax'))
    series.sax_2 = list(df["0_sax"].values)

    return series, breakpoints_2


def calculate_breakpoints(ts, alphabet_size):
    if p.kind_of_breakpoints == "linear":
        area = max(ts) - min(ts)
        section = area / alphabet_size
        breakpoints = []
        for i in range(alphabet_size):
            breakpoints.append(round(min(ts) + section * i, 2))

    elif p.kind_of_breakpoints == "statistical":
        breakpoints = cuts_for_asize(alphabet_size)
        breakpoints[0] = min(ts)

    elif p.kind_of_breakpoints == "density":
        breakpoints = np.quantile(ts, np.linspace(0, p.quantil, alphabet_size))

    return breakpoints


def apply_sax(series):
    breakpoints = calculate_breakpoints(series.ts_norm, series.alphabet_size)
    series.sax = list(ts_to_string(series.ts_norm, breakpoints))
    series.len_sax = len(series.sax)
    if series.double:
        series, breakpoints_2 = get_sax_2(series, breakpoints)

    return series


