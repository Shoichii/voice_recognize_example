# Используем официальный Python образ в качестве базового
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости и удаляем временные файлы
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        portaudio19-dev \
        libffi-dev \
        libssl-dev \
        alsa-utils \
        libasound2 \
        libasound2-dev \
        pulseaudio \
        && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в контейнер
COPY reqs.txt .

# Устанавливаем pip до последней версии
RUN pip install --upgrade pip

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r reqs.txt

# Копируем остальные файлы проекта в контейнер
COPY main.py .
COPY large/ ./large/

# Указываем команду для запуска приложения с отключенной буферизацией вывода
CMD ["python", "-u", "main.py"]
