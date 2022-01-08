import pandas as pd
import numpy as np
from saxpy.znorm import znorm
import random
from scipy.io import arff
from preprocessing.preprocess_data import preprocess_data
import params as p
from sklearn.decomposition import PCA


def read_data(index):
    if index == "ecg":
        df = pd.read_csv('data/ecg_2.csv', header=None)
        ts = df.values.tolist()
        ts = ts[2:9] + ts[10:11] + ts[12:13] + ts[15:16]
        ts = sum(ts, [])
    elif index == "olive":
        ts = np.loadtxt('/Users/steffi/Downloads/OliveOil/OliveOil_Test.txt')
        ts = ts[0: 10].tolist()
        ts = [j for i in ts for j in i]
    elif index == "coffee":
        ts = np.loadtxt('/Users/steffi/Downloads/Coffee/Coffee_TEST.txt')
        ts = ts[0:11].tolist()
        ts = [j for i in ts for j in i]
    elif index == "traveled_miles":
        df = pd.read_csv('data/trav_miles_long.csv')
        ts = list(df['TRFVOLUSM227NFWA'])
        ts = np.array(ts)
        ts = ts[0:588]

    ts_norm = preprocess_data(ts)
    print("len", len(ts_norm))
    #ts = ts[0:100]
   # ts_norm = ts_norm[0:100]
    return ts, ts_norm


def read_data2(index):
    if index == "ecg":
        df = pd.read_csv('data/ecg_2.csv', header=None)
        ts = df.values.tolist()
        ts = ts[2:9] + ts[10:11] + ts[12:13] + ts[15:17] + ts[52:59]
       # ts = ts[40:60]
        ts = sum(ts, [])
        #ts = ts[0:80]
        #ts = ts[0:13] + ts[43:46]
    elif index == "olive":
        ts = np.loadtxt('/Users/steffi/Downloads/OliveOil/OliveOil_Test.txt')
        ts = ts[0: 30].tolist()
        ts = [j for i in ts for j in i]
    elif index == "coffee":
        ts = np.loadtxt('/Users/steffi/Downloads/Coffee/Coffee_TRAIN.txt')
        ts = ts[0:60].tolist()
        ts2 = np.loadtxt('/Users/steffi/Downloads/Coffee/Coffee_TRAIN.txt')
        ts2 = ts2[0:20].tolist()
        ts = [j for i in ts for j in i]
        ts2 = [j for i in ts2 for j in i]
        ts = ts + ts2
    elif index == "traveled_miles":
        df = pd.read_csv('data/Miles_Traveled.csv')
        ts = list(df['TRFVOLUSM227NFWA'])

    elif index == "traveled_miles_long":
        df = pd.read_csv('data/trav_miles_long.csv')
        ts = list(df['TRFVOLUSM227NFWA'])

    elif index == "random":
        randomlist = []
        for i in range(0, 2000):
            n = random.randint(1, 30)
            randomlist.append(n)
            ts = randomlist

    elif index == "eyes_pca":
        path = "/Users/steffi/PycharmProjects/MDL_Clustering/MDL_PULP_MOTIF_DETECTION/data/EyesOpenShut.arff"
        data1 = arff.loadarff(open(path, 'rt'))
        list_to_append = list(range(80))
        list_to_append2 = list(range(3))
        df = pd.DataFrame()
        for i in list_to_append:
            i = i
            for j in list_to_append2:
                j = j + 7
                df1 = data1[0][i][0][j]

                df[i] = list(df1)
        df = np.array(df).astype("int")
        pca = PCA(n_components=28).fit(df)
        ts = pca.transform(df.data)
        ts = ts.reshape(1,-1)[0]


    elif index =="eyes":
        ts = []
        path = "/Users/steffi/PycharmProjects/MDL_Clustering/MDL_PULP_MOTIF_DETECTION/data/EyesOpenShut.arff"
        data1 = arff.loadarff(open(path, 'rt'))
        list_to_append = list(range(30))
        list_to_append2 = list(range(14))
        for i in list_to_append:
            for j in list_to_append2:
                df1 = data1[0][i][0][j]
                print(len(ts))
                ts.extend(df1)
        ts = ts

    elif index == "beer":
        df = pd.read_csv(
            '/Users/steffi/PycharmProjects/MDL_Clustering/MDL_PULP_MOTIF_DETECTION/data/BeerWineLiquor.csv')
        ts = list(df['beer'])

    elif index == "Stand":
        path = "/Users/steffi/PycharmProjects/MDL/data/StandWalkJumpDimension1_TEST.arff"
        ts = []
        data1 = arff.loadarff(open(path, 'rt'))
        list_to_append = list(range(3))
        list_to_append = [2,3,7,14] #13
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
        ts.extend(data[0: 30].tolist())
        ts = [j for i in ts for j in i]

    elif index == "faces":
        path = "/Users/steffi/PycharmProjects/MDL_Clustering/MDL_PULP_MOTIF_DETECTION/data/FaceAll_TRAIN.txt"
        ts = []
        data = np.loadtxt(path)
        ts.extend(data[0: 20].tolist())
        ts = [j for i in ts for j in i]

    elif index == "random":
        randomlist = []
        for i in range(0,2000):
            n = random.randint(1,30)
            randomlist.append(n)
            ts = randomlist


    elif index == "ecg5D":
        path = "/Users/steffi/PycharmProjects/MDL/data/ECGFiveDays_TRAIN.txt"
        ts = []
        data = np.loadtxt(path)
        ts.extend(data[0: 20].tolist())
        ts = [j for i in ts for j in i]

    ts = np.array(ts)
    #ts = znorm(ts)
    #if index =="olive":
    #    pass
    #elif len(ts > 1000):
    #ts = ts[0:3000]
   # else:
    #    ts = ts[0:300]
    leng = 100
    ts_norm = preprocess_data(ts)
    print("len", len(ts_norm))
    ts_norm = ts_norm[0:leng]
    ts = ts[0:leng*p.number_to_reduce]

    return ts, ts_norm
