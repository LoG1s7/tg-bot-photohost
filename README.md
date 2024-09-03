# Telegram Photohost Bot

## Описание

Этот проект представляет собой Telegram-бота, который позволяет пользователям загружать фотографии и просматривать их через веб-интерфейс на Flask. Бот включает функции подтверждения доступа пользователей и возможность загружать несколько фотографий одновременно.

## Используемые технологии

- **Python**: Основной язык программирования
- **aiogram**: Библиотека для работы с Telegram Bot API
- **Flask**: Веб-фреймворк для создания веб-приложений
- **python-dotenv**: Для загрузки переменных окружения из файла `.env`
- **Docker**: Для контейнеризации приложения
- **Docker Compose**: Для управления многоконтейнерными приложениями
- **APScheduler**: Для отложенной задачи удаления фото старше 1 месяца

## Установка и развертывание

### Предварительные требования

- Установленный Docker
- Установленный Docker Compose

### Шаги для развертывания

1. **Клонируйте репозиторий**:

   ```bash
   git clone https://github.com/LoG1s7/tg-bot-photohost.git
   cd tg-bot-photohost
   ```

2. **Создайте файл `.env`**:

   В корне проекта создайте файл `.env` и добавьте следующие конфигурации:

   ```plaintext
   API_TOKEN=YOUR_BOT_API_TOKEN
   ADMIN_ID=YOUR_ADMIN_ID
   UPLOAD_FOLDER=uploads/
   ```

   Замените `YOUR_BOT_API_TOKEN` на токен вашего Telegram-бота и `YOUR_ADMIN_ID` на ID администратора.

3. **Постройте и запустите контейнер**:

   Выполните команды:

   ```bash
   docker-compose build
   docker-compose up
   ```

4. **Доступ к приложению**:

   После успешного запуска контейнера вы сможете получить доступ к Flask приложению по адресу:

   ```plaintext
   http://localhost:5000/view_photos
   ```

5. **Использование Telegram-бота**:

   - Запустите бота в Telegram, используя команду `/start`.
   - После получения подтверждения от администратора, используйте команду `/add_photo`, чтобы загрузить фотографии.

## Структура проекта

```
/telegram_photo_bot/
├── bot.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── handlers/
│   ├── __init__.py
│   ├── photo_handlers.py
│   └── start_handlers.py
├── main.py
├── templates/
│   └── view_photos.html
└── static/
    └── uploads/
```

### Папки и файлы:

- **bot.py**: Основная логика бота
- **handlers/**: Обработчики для команд бота
- **main.py**: Точка входа приложения
- **templates/**: Шаблоны для Flask-прилодения
- **static/uploads/**: Директория для сохранения загруженных фотографий

## Автор
[Aleksandr Kolesnikov](https://github.com/log1s7)
