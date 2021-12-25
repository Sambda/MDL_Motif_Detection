import pandas as pd
import numpy as np
from saxpy.znorm import znorm
import random
from scipy.io import arff
from preprocessing.preprocess_data import preprocess_data


def read_data(index):
    if index == "ecg":
        df = pd.read_csv('data/ecg_2.csv', header=None)
        ts = df.values.tolist()
        ts = ts[0:20]
        ts = sum(ts, [])
    elif index == "olive":
        ts = np.loadtxt('/Users/steffi/Downloads/OliveOil/OliveOil_Test.txt')
        ts = ts[0: 20].tolist()
        ts = [j for i in ts for j in i]
    elif index == "coffee":
        ts = np.loadtxt('/Users/steffi/Downloads/Coffee/Coffee_TEST.txt')
        ts = ts[0:10].tolist()
        ts = [j for i in ts for j in i]
    elif index == "traveled_miles":
        df = pd.read_csv('data/Miles_Traveled.csv')
        ts = list(df['TRFVOLUSM227NFWA'])
    elif index == "random":
        randomlist = []
        for i in range(0, 2000):
            n = random.randint(1, 30)
            randomlist.append(n)
            ts = randomlist

    elif index == "beer":
        df = pd.read_csv(
            '/Users/steffi/PycharmProjects/MDL_Clustering/MDL_PULP_MOTIF_DETECTION/data/BeerWineLiquor.csv')
        ts = list(df['beer'])

    elif index == "Stand":
        path = "/Users/steffi/PycharmProjects/MDL/data/StandWalkJumpDimension1_TEST.arff"
        ts = []
        data1 = arff.loadarff(open(path, 'rt'))
        list_to_append = list(range(2))
        for i in list_to_append:
            df1 = list(data1[0][i])[:-1]
            print(list(data1[0][i])[-1])
            ts.extend(df1)
    if index == "Wafer":
        path = "/Users/steffi/PycharmProjects/MDL_Clustering/MDL_PULP_MOTIF_DETECTION/data/Wafer_TRAIN.txt"
        data = np.loadtxt(path)
        # for i in range(10):
        ts = data[20: 35].tolist()
        ts = [j for i in ts for j in i]

    elif index == "ethanol":
        path = "/Users/steffi/PycharmProjects/MDL_Clustering/MDL_PULP_MOTIF_DETECTION/data/EthanolLevel_TRAIN.txt"
        # ts = np.loadtxt(path)
        # ts1 = ts[10: 60].tolist()
        # ts1 = [j for i in ts1 for j in i]
        ts = []
        data = np.loadtxt(path)
        # for i in range(300):
        ts.extend(data[0: 15].tolist())
        ts = [j for i in ts for j in i]

    elif index == "faces":
        path = "/Users/steffi/PycharmProjects/MDL_Clustering/MDL_PULP_MOTIF_DETECTION/data/FaceAll_TRAIN.txt"
        ts = []
        data = np.loadtxt(path)
        ts.extend(data[0: 20].tolist())
        ts = [j for i in ts for j in i]

    elif index == "eyes":
        ts = []
        data1 = arff.loadarff(open(path, 'rt'))
        list_to_append = list(range(5))
        list_to_append2 = list(range(14))
        df1 = []
        for i in list_to_append:
            for j in list_to_append2:
                df1 = data1[0][i][0][j]
                ts.extend(df1)

    elif index == "ecg5D":
        path = "/Users/steffi/PycharmProjects/MDL/data/ECGFiveDays_TRAIN.txt"
        ts = []
        data = np.loadtxt(path)
        ts.extend(data[0: 20].tolist())
        ts = [j for i in ts for j in i]

    ts = np.array(ts)
    ts = znorm(ts)

    if index =="olive":
        pass
    elif len(ts > 1000):
        ts = ts[0:2500]
    else:
        ts = ts[0:300]

    ts_norm = preprocess_data(ts)

    return ts, ts_norm