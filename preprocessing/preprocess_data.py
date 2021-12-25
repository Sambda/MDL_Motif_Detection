import numpy as np
from saxpy.znorm import znorm
from scipy.stats import boxcox
import params as p
from tsmoothie.smoother import LowessSmoother
from preprocessing.get_data import get_ts
from plot import simple_plot
from pyts.approximation import PiecewiseAggregateApproximation



def power_transformation(ts):
    min_ts = abs(min(ts))+0.1
    ts = [x+min_ts for x in ts]
    s, _ = boxcox(ts)
    return s


def get_number_for_reducing(len_ts):
    for number_to_reduce in range(1, 64):
        if len_ts/number_to_reduce < p.max_series_length:
            return number_to_reduce


def paa(ts):
    ts_paa = []
    if p.reduce_ts_with_max_series_length:
        paa_reduction = get_number_for_reducing(len(ts))
    else:
        paa_reduction = p.number_to_reduce
    for i in range(1, len(ts) - 1, paa_reduction):
        mean = np.mean([ts[i - 1], ts[i], ts[i + 1]])
        ts_paa.append(mean)
    return list(ts_paa), paa_reduction


def get_ts_paa(ts):
    if p.reduce_ts_with_max_series_length:
        reduce_size = get_number_for_reducing(len(ts))
    else:
        reduce_size = p.number_to_reduce
    transformer = PiecewiseAggregateApproximation(window_size=reduce_size)
    ts_paa = list(transformer.transform([ts])[0])
    #ts_paa_long = [reduce_size*[i] for i in ts_paa]
    #ts_paa_long = sum(ts_paa_long, [])
    return ts_paa,reduce_size


def smooth_data(data):
    smooth_fraction = p.smooth_fraction

    # operate smoothing
    smoother = LowessSmoother(smooth_fraction=smooth_fraction, iterations=1)
    smoother.smooth(data)

    return list(smoother.smooth_data[0])


def preprocess_data(ts):
    paa_reduction = 0

    # PAA on TS
    if p.paa:
        ts, paa_reduction = get_ts_paa(ts)
        #simple_plot(ts, "paa")

    # Normalise Data
    if p.z_norm:
        ts = znorm(ts)
        #simple_plot(ts, "z_norm")

    # Smooth TS
    if p.smooth_fraction:
        ts = smooth_data(ts)
        #simple_plot(ts, "smooth_fraction")

    # Differencing
    if p.differencing:
        ts = np.array(ts)
        ts = ts[1:] - ts[:-1]
        #simple_plot(ts,"differencing")

    # Power Transformation on TS
    if p.power_transformation:
        ts = power_transformation(ts)
        #simple_plot(ts, "power_transformation")

    return ts


def read_data(data_number):
    ts = get_ts(data_number)
    ts_norm = preprocess_data(ts)
    return ts, ts_norm
