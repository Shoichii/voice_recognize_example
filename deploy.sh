#!/bin/bash

set -e

# Переменные
IMAGE_NAME="vv_cook_img"
CONTAINER_NAME="vv_cook_container"

# Функция для установки Docker
install_docker() {
    echo "Устанавливаем Docker..."

    sudo apt update
    sudo apt install -y ca-certificates curl gnupg lsb-release

    # Добавляем официальный GPG ключ Docker
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    # Устанавливаем стабильный репозиторий Docker
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt update

    # Устанавливаем Docker Engine и связанные компоненты
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Включаем и запускаем Docker
    sudo systemctl enable docker
    sudo systemctl start docker

    echo "Docker установлен успешно."
}

# Функция для проверки установки Docker
check_docker() {
    if ! command -v docker &> /dev/null
    then
        install_docker
    else
        echo "Docker уже установлен."
    fi
}

# Функция для построения Docker образа
build_docker_image() {
    echo "Построение Docker образа без использования кэша..."
    sudo docker build --no-cache -t "$IMAGE_NAME" .
    echo "Docker образ '$IMAGE_NAME' успешно построен."
}

# Функция для запуска Docker контейнера
run_docker_container() {
    echo "Запуск Docker контейнера..."

    # Проверяем, существует ли уже контейнер с таким именем
    if sudo docker ps -a --format '{{.Names}}' | grep -Eq "^${CONTAINER_NAME}\$"; then
        echo "Контейнер '$CONTAINER_NAME' уже существует. Останавливаем и удаляем его..."
        sudo docker rm -f "$CONTAINER_NAME"
    fi

    # Определяем путь к PulseAudio сокету на хосте
    PULSE_SOCKET="/run/user/$(id -u)/pulse/native"

    # Запуск контейнера с доступом к PulseAudio сокету
    sudo docker run -d \
        --name "$CONTAINER_NAME" \
        --device /dev/snd \
        --group-add audio \
        -v "$PULSE_SOCKET":/run/pulse/native \
        -e PULSE_SERVER=unix:/run/pulse/native \
        "$IMAGE_NAME"

    echo "Docker контейнер '$CONTAINER_NAME' запущен."
}

# Основная часть скрипта
check_docker
build_docker_image
run_docker_container

echo "Развёртывание завершено успешно."
