from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
import librosa
from users.models import Users
from tensorflow.keras.models import load_model
import h5py
import numpy as np
import tensorflow as tf
from pydub import AudioSegment
import soundfile as sf
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# model = h5py.File('model.h5','r+')



def detect(request):
    sender_token = request.COOKIES['token']
    try:
        sender = Users.objects.get(token=sender_token)
        if request.method == 'POST':
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)
            # mfcc = convert(filename)
            model = get_model('model.h5')
            data = prepare(filename)
            prediction = predict(model,data)
            Genre = get_name(prediction)

            return render(request,'result.html',context={
                                                        'Genre' : Genre
                                                         })

        else:
            return render(request,'home.html',context=None)

    except:
        return redirect('/')

def convert(location):
    signal, sampleRate = librosa.load(location, sr=22050)
    mfcc = librosa.feature.mfcc(signal, sampleRate, n_mfcc=13, n_fft=2048, hop_length=512)
    mfcc = mfcc.T.tolist()
    return mfcc


# def predict(model,X):
#     #change axis to 4
#     X = np.array([X])
#     # X = X.reshape([1] + list(X.shape))
#     print(X.shape)
#     X = tf.expand_dims(X,axis = -1)
#     print(X.shape)
#
#     X = X[...,np.newaxis]
#     # X = X.reshape(list(X.shape) + [1])
#     # X = X[np.newaxis,...]
#
#     #predict label
#     prediction = model.predict(X)
#     #get highest prob
#     prediction = np.argmax(prediction,axis=1)
#
#     return prediction
def predict(model,X):
    #change axis to 4
    vector = np.zeros((10))
    X = np.array(X)
    for x in X:
        x = np.array([x])

        X = tf.expand_dims(x,axis = -1)

        x = x[...,np.newaxis]

        prediction = model.predict(x)
        vector = np.add(vector,prediction)

    prediction = np.argmax(vector,axis=1)

    return prediction


def prepare(filename):
    list = []
    f = sf.SoundFile(filename)
    time = (len(f)/f.samplerate)
    time = time // 3
    for i in range(int(time)):
        t1 = 3 * i
        t2 = 3 *(i + 1)

        ffmpeg_extract_subclip(filename,t1,t2,targetname='newSong%s.wav'%i)
        list.append(convert('newSong%s.wav'%i))

    return list




def get_model(name):
    model = load_model(name)
    return model

def get_name(number):
    mapping= [
        "blues",
        "classical",
        "country",
        "disco",
        "hiphop",
        "jazz",
        "metal",
        "pop",
        "reggae",
        "rock"
    ]
    return mapping[number[0]]
