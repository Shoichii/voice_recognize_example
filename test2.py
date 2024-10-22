import json
import pyaudio
import wave
from vosk import Model, KaldiRecognizer
from threading import Thread, Event

# Глобальные переменные для управления воспроизведением
start_listening_event = Event()
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
    while data and start_listening_event.is_set():
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

    print('начинаю слушать всё')

    # try:
    while True:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                answer = json.loads(rec.Result())
                if answer['text']:
                    print(f"Весь распознанный текст: {answer['text']}")
                    if 'рецепт' in answer['text']:
                        start_listening_event.set()
                        print('начинаю слушать команды')
                    if "остановись" in answer['text']:
                        start_listening_event.clear()
                        print('прекращаю слушать команды')
                        break
                    # Если обнаружено, что это один из рецептов
                    list_recipes = ('пельмени', 'блины')
                    if answer['text'] in list_recipes and start_listening_event.is_set():
                        # Запускаем воспроизведение в отдельном потоке
                        audio_thread = Thread(
                            target=play_audio, args=(answer['text'],))
                        audio_thread.start()

    # except KeyboardInterrupt:
    #     stop_event.set()
    # finally:
    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()


if __name__ == '__main__':
    listen()
