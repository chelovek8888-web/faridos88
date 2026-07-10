# Telegram Image Search Bot

Бот Telegram для поиска похожих товаров по фотографии.

## Возможности

- Поиск похожих изображений по фотографии
- Использование OpenCLIP для получения эмбеддингов
- Быстрый поиск через FAISS
- Индексация изображений из Telegram-каналов
- Работа через aiogram и Telethon

## Структура проекта

```
bot.py                 # Telegram-бот
search.py              # Поиск похожих изображений
config.py              # Настройки проекта
channels.py            # Список каналов

build_index_v2.py      # Построение индекса
build_faiss_index.py   # Создание FAISS
rebuild_faiss.py       # Перестроение индекса
```

## Установка

Создать виртуальное окружение:

```bash
python3 -m venv venv
```

Активировать:

```bash
source venv/bin/activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python bot.py
```

## Используемые технологии

- Python
- aiogram
- Telethon
- OpenCLIP
- FAISS
- Pillow
- NumPy
- Torch

## В репозиторий не входят

- session.session
- index.faiss
- index.pkl
- meta.json
- progress.json

Эти файлы создаются локально.
