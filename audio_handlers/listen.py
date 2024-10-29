import pyaudio
import json
from threading import Thread
import loader
from text_handlers import get_keyphrase, get_answer_data
from play_stream import play_audio


def listen():
    """Функция для прослушивания аудио с микрофона."""
    # инициализация потока прослушивания
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1,
                    rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print('начинаю слушать всё')

    # бесконечный цикл прослушивания
    while True:
        # бесконечный цикл прослушивания
        # для одного одновременного сценария
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if loader.rec.AcceptWaveform(data):
                answer = json.loads(loader.rec.Result())

                # если есть распознавание
                if answer['text']:
                    # принт просто для обзора текста
                    print(f"Весь распознанный текст: {answer['text']}")

                    # включение/выключение прослушивания команд
                    if 'рецепт' in answer['text'] and not loader.start_listening_event.is_set():
                        loader.start_listening_event.set()
                        print('начинаю слушать команды')
                        break
                    if "отмен" in answer['text']:
                        loader.commands_pause_event.clear()
                        loader.start_listening_event.clear()
                        print('прекращаю слушать команды')
                        break

                    # слушаем команды
                    if not loader.commands_pause_event.is_set() \
                            and loader.start_listening_event.is_set():
                        # ловим фразу и разбиваем на ключевые слова
                        keyphrase = get_keyphrase(answer['text'])
                        # определяем какой рецепт
                        answer_data = get_answer_data(keyphrase)
                        print('answer_data', answer_data)
                        number_of_matches = 0
                        if answer_data:
                            number_of_matches = len(answer_data)
                            print(f'Найдено {number_of_matches} совпадений')
                            # тут наверно можно говорить дальше и дальше
                            # пока не будет услышан нужный вариант
                            # либо отменить вовсе и перефразировать вопрос
                            best_result = answer_data[0][0]
                            track_name = ''
                            for item in loader.db_list_keyphrases:
                                if item.get('keyphrase') == best_result:
                                    track_name = item.get('answer')
                                    break
                            if track_name:
                                # Запускаем воспроизведение
                                # аудио в отдельном потоке
                                loader.commands_pause_event.set()
                                audio_thread = Thread(
                                    target=play_audio, args=(track_name,))
                                audio_thread.start()
                        else:
                            print('Не найдено совпадений')
                        break
