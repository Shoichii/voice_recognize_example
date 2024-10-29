import pyttsx3

# Инициализация синтезатора речи
engine = pyttsx3.init()

# Настройка параметров голоса
engine.setProperty("rate", 200)  # Скорость речи
engine.setProperty("volume", 1)  # Громкость (от 0 до 1)

# Текст для озвучивания
text = "Привет, как у тебя дела?"

# Озвучка текста
engine.say(text)
engine.runAndWait()
