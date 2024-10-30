from vosk import KaldiRecognizer, Model
import pyaudio
from threading import Event
import spacy

# инициализация потока прослушивания
start_listening_event = Event()
playing_audio_event = Event()
model = Model("small")
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()

# Загрузка модели для русского языка
nlp = spacy.load("ru_core_news_sm")

# список ключевых слов из бд
db_list_keyphrases = []

# пороговое значение
threshold_1 = 60  # для fuzzywuzzy - sort_results ф-ия
threshold_2 = 80  # для цикла for
