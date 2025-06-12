# Sleep Trekking Bot

## Инструкции по установке (Windows)
1. Создайте .env файл
2. Скопируйте .env-example в .env и заполните токеном от BotFather в телеграм
3. Перейдите в Powershell в папку с проектом и создайте виртуальное окружение

```python3 -m venv venv"```

4. Активируйте виртуальное окружение

```.\.venv\Scripts\Activate```

5. Установите зависимости

```pip3 install -r requirements.txt```

6. Создайте БД SQLite

```sqlite3 sleep_bot.db ".databases"```

7. Запустите бота
```python3 bot.py```

