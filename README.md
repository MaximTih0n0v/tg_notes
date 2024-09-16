# Project Name

Описание вашего проекта и его основное предназначение.

## Оглавление

1. [Описание](#описание)
2. [Функции](#функции)
3. [Требования](#требования)
4. [Установка](#установка)
5. [Использование](#использование)


## Описание

Бот на Python, использующий FastAPI, SQLAlchemy, PostgreSQL и aiogram для управления заметками и взаимодействия с пользователями через Telegram.

## Функции

- Создание, редактирование и удаление заметок.
- Поиск заметок по тегам.
- Просмотр заметок
- Управление заметками пользователя через Telegram-бота.
- Логирование действий и ошибок.

## Требования

- Python 3.9+
- PostgreSQL
- Docker
- Зависимости из `requirements.txt`

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/MaximTih0n0v/tg_notes.git
    cd yourproject
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```

3. Настройте переменные окружения. Создайте файл `.env` и добавьте следующие переменные:

    ```env
    TELEGRAM_TOKEN=your_telegram_token
    DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
    DB_NAME=database_name
    DB_USER=database_username
    DB_PASSWORD=database_password
    DB_PORT=database_port
    DB_HOST=database_host
    ```


4. Запустите приложение:

    ```bash
    docker-compose up --build

    ```


## Использование

После запуска приложения вы можете взаимодействовать с ботом в Telegram. Используйте команды:

- `/add_note` - Создать новую заметку.
- `/my_notes` - Просмотреть свои заметки.
- `/edit_note` - Редактировать существующую заметку.
- `/delete_note` - Удалить заметку.
- `/search_by_tag` - Найти заметки по тегу или тегам.


