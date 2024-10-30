import wave
import pyaudio
import loader


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
    while data and loader.start_listening_event.is_set():
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()
    # print('play audio 1', loader.playing_audio_event.is_set())
    loader.playing_audio_event.clear()
    # print('play audio 2', loader.playing_audio_event.is_set())
