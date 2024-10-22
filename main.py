import json
import pyaudio
from vosk import Model, KaldiRecognizer
import wave
from play_stream import play_track


print('start')
model = Model("small")
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1,
                rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def listen():
    print('начинаю слушать')
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(rec.Result())
            list_recipes = ('пельмени', 'блины')
            if answer['text']:
                print(answer['text'])
            if answer['text'] and answer['text'] in list_recipes:
                yield play_track(answer['text'])


for text in listen():
    print(text)
