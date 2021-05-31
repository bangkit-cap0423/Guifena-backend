from api.models import Incidents
import librosa.display
import os
import gc
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import base64
from datetime import datetime, timedelta
from pyfcm import FCMNotification
from .models import Incidents, Sensors, Token
import api.constanta as const
# THIS IS WHERE ML CLASSIFICATION WILL HAPPEN


def extract_spectrogram(fname, iname):
    audio, sr = librosa.load(fname, res_type='kaiser_fast')
    S = librosa.feature.melspectrogram(audio, sr=sr, n_mels=128)
    log_S = librosa.power_to_db(S, ref=np.max)
    fig = plt.figure(figsize=[1, 1])
    ax = fig.add_subplot(111)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.axis("off")
    ax.axis("tight")
    plt.margins(0)
    librosa.display.specshow(log_S, sr=sr)
    fig.savefig(iname, dpi=100, pad_inches=0)


def printToConsole(payload: str, time, sensorId):

    f = f'{str(datetime.now())}_sensor1.m4a'
    wav_file = open(
        f'/home/a2292233/guifena/Guifena-backend/guifena/api/input/{f}', "wb")
    decode_string = base64.b64decode(payload)
    wav_file.write(decode_string)
    fimg = f.replace('.m4a', '.png')
    extract_spectrogram(
        f'/home/a2292233/guifena/Guifena-backend/guifena/api/input/{f}', f"/home/a2292233/guifena/Guifena-backend/guifena/api/predict_img/{fimg}")
    input = []
    input.append(tf.keras.preprocessing.image.img_to_array(
        tf.keras.preprocessing.image.load_img(f"/home/a2292233/guifena/Guifena-backend/guifena/api/predict_img/{fimg}", target_size=(100, 100))))
    input = np.array(input)
    model1 = keras.models.load_model(
        '/home/a2292233/guifena/Guifena-backend/guifena/api/model/')
    chainsaw_detect = model1.predict_classes(input)
    chainsaw_detect = chainsaw_detect[0][0]
    if (chainsaw_detect == 1):
        # INCIDENT DETECTED
        sensor = Sensors.objects.get(id=sensorId)
        Incidents.objects.create(
            sensor=sensor,
            status=1,
            timestamp=time
        )
        sendNotification()


def sendNotification():
    api_key = 'AAAAej261Qg:APA91bFNLBEeIl_ZPTi98ct_fudgnUDsVEE8Xd7mB9azDSGk5Hu8xJWc8AO6AvNohdySg9hJe7uSdyTwUsoehGKzYbr8JOMZmoVv0Vm3SWmiqlEhy0iFOqB1wMGEgzAMRseJNokpFIPF'
    tokens = []
    query_token = Token.objects.all()
    for query in query_token:
        tokens.append(query.token)
    push_service = FCMNotification(api_key=api_key)
    data_message = {
        "raisa": 'ok',

    }
    push_service.notify_multiple_devices(
        registration_ids=tokens, data_message=data_message)


def CheckSensorPeriodic():
    sensors = Sensors.objects.all()
    now = datetime.now()
    created_time = now - timedelta(minutes=10)
    for sensor in sensors:
        timestamp = sensor.last_seen
        if time_in_range(now, created_time, timestamp):
            sensor.status = const.STATUS_ONLINE
            sensor.save()
        else:
            sensor.status = const.STATUS_OFFLINE
            sensor.save()


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
