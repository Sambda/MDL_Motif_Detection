import librosa
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from sklearn.decomposition import PCA


def load_with_librosa(path):
    x, sr = librosa.load(path, sr=None)
    x = librosa.feature.mfcc(y=x, sr=sr/0.001)
    return x[0]



