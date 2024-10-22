import json
import pyaudio
import wave
from vosk import Model, KaldiRecognizer
from threading import Thread, Event

# Глобальная переменная для управления воспроизведением
stop_event = Event()


def play_audio(name):
    """Функция для воспроизведения аудио."""
    chunk = 1024
    wf = wave.open(f"./media/{name}.wav", "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()


def listen():
    """Функция для прослушивания аудио с микрофона."""
    model = Model("small")
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1,
                    rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print('начинаю слушать')

    while not stop_event.is_set():
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            answer = json.loads(rec.Result())
            if answer['text']:
                print(f"Распознано: {answer['text']}")
                if answer['text'] == "стоп":
                    stop_event.set()
                    return
                # Если обнаружено, что это один из рецептов
                list_recipes = ('пельмени', 'блины')
                if answer['text'] in list_recipes:
                    # Запускаем воспроизведение в отдельном потоке
                    audio_thread = Thread(
                        target=play_audio, args=(answer['text'],))
                    audio_thread.start()

    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == '__main__':
    listen()
