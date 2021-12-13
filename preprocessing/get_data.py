import numpy as np
import pandas as pd

def get_ts(index):

    if index == "sinus":
        t = np.arange(0, 398, 0.2)
        ts = np.sin(t)

    elif index == "ecg":
        df = pd.read_csv('data/ecg_2.csv', header=None)
        ts = df.values.tolist()
        ts = ts[0:5]
        ts = sum(ts, [])

    elif index == "coffee":
        ts = np.loadtxt('/Users/steffi/Downloads/Coffee/Coffee_TEST.txt')
        ts = ts[0:100].tolist()
        ts = [j for i in ts for j in i]

    elif index == "olive_oil":
        ts = np.loadtxt('/Users/steffi/Downloads/OliveOil/OliveOil_Test.txt')
        ts = ts[0: 10].tolist()
        ts = [j for i in ts for j in i]

    if index == "traveled_miles":
        df = pd.read_csv('data/Miles_Traveled.csv')
        ts = list(df['TRFVOLUSM227NFWA'][240:480])

    return ts