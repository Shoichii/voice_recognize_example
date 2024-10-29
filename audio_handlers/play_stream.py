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

    loader.commands_pause_event.clear()
    stream.stop_stream()
    stream.close()
    p.terminate()
