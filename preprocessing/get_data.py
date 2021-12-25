import numpy as np
import pandas as pd
from scipy.io import arff
from preprocessing.load_audio_data import load_with_librosa

def get_ts(index):

    if index == "sinus":
        t = np.arange(0, 398, 0.2)
        ts = np.sin(t)

    elif index == "ecg":
        df = pd.read_csv('data/ecg_2.csv', header=None)
        ts = df.values.tolist()
        #ts = ts[0:10]
        ts = ts[20:30]
        ts = sum(ts, [])

    elif index == "coffee":
        ts = np.loadtxt('/Users/steffi/Downloads/Coffee/Coffee_TEST.txt')
        ts = ts[0:100].tolist()
        ts = [j for i in ts for j in i]

    elif index == "olive_oil":
        ts = np.loadtxt('/Users/steffi/Downloads/OliveOil/OliveOil_Test.txt')
        ts = ts[0: 10].tolist()
        ts = [j for i in ts for j in i]

    elif index == "shampoo":
        ts = pd.read_csv("data/shampoo.csv")
        ts = np.array(ts['Sales'])

    elif index == "ham":
        ts = np.loadtxt('/Users/steffi/PycharmProjects/MDL/data/HAM.txt')
        ts = ts[0:10].tolist()
        ts = [j for i in ts for j in i]

    elif index == "ecg5D":
        path = "/Users/steffi/PycharmProjects/MDL/data/ECGFiveDays_TRAIN.txt"
        ts = []
        data = np.loadtxt(path)
        #ts.extend(data[0: 20].tolist())
        ts.extend(data[20: 40].tolist())
        ts = [j for i in ts for j in i]


    elif index == "faces":
        path = "/Users/steffi/PycharmProjects/MDL_Clustering/MDL_PULP_MOTIF_DETECTION/data/FaceAll_TRAIN.txt"
        ts = []
        data = np.loadtxt(path)
        ts.extend(data[0: 20].tolist())
        ts = [j for i in ts for j in i]

    if index == "traveled_miles":
        df = pd.read_csv('data/Miles_Traveled.csv')
        ts = list(df['TRFVOLUSM227NFWA'][240:480])

    elif index == "beer":
        df = pd.read_csv(
            '/Users/steffi/PycharmProjects/MDL_Clustering/MDL_PULP_MOTIF_DETECTION/data/BeerWineLiquor.csv')
        ts = list(df['beer'])

    elif index == "Ethanol":
        path = "/Users/steffi/PycharmProjects/MDL_Clustering/MDL_PULP_MOTIF_DETECTION/data/EthanolLevel_TRAIN.txt"
        ts = np.loadtxt(path)
        ts = ts[0: 20].tolist()
        ts = [j for i in ts for j in i]

    elif index =="StandWalkJump":
        path = "/Users/steffi/PycharmProjects/MDL/data/StandWalkJumpDimension1_TEST.arff"
        ts = []
        data1 = arff.loadarff(open(path, 'rt'))
        list_to_append = list(range(2))
        for i in list_to_append:
            df1 = list(data1[0][i])[:-1]
            ts.extend(df1)
        ts = ts[0:3500]

    elif index == "audio":
        path = "data/mdl6.wav" #mdl3 #mdl6
        ts = load_with_librosa(path)

    return ts