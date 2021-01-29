import librosa

#location = "sample.wav"
def convert(location):
    signal, sampleRate = librosa.load(location, sr=22050)
    mfcc = librosa.feature.mfcc(signal, sampleRate, n_mfcc=13, n_fft=2048, hop_length=512)
    mfcc = mfcc.T.tolist()
    return mfcc