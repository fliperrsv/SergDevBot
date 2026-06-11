```markdown
# 🤖 Сергей Резунков – Telegram-бот портфолио

[![Bot](https://img.shields.io/badge/Telegram-Бот-0088cc?style=flat-square&logo=telegram)](https://t.me/ваш_бот_username)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.10-00a98f?style=flat-square)](https://docs.aiogram.dev/)

**Многофункциональный Telegram-бот** для демонстрации навыков веб-разработчика. Бот показывает портфолио, отвечает на вопросы, хранит пользователей в базе данных и поддерживает напоминания.

🔗 **Тест-бот:** [https://t.me/ваш_бот_username](https://t.me/ваш_бот_username)

---

## 📦 Возможности

- ✅ Приветствие с кнопками (контакты, услуги, портфолио)
- ✅ Инлайн-клавиатуры и callback-запросы
- ✅ Поддержка нескольких языков (русский / английский)
- ✅ База данных SQLite (пользователи, напоминания, премиум-статус)
- ✅ Напоминания (установка даты и времени)
- ✅ Премиум-доступ (заглушка для будущей монетизации)
- ✅ Администраторские функции (статистика, рассылка)
- ✅ Фоновые задачи (автопроверка напоминаний)
- ✅ Логирование ошибок

---

## 🛠 Технологии

- **Python 3.10+** – основной язык
- **Aiogram 3.x** – фреймворк для Telegram Bot API
- **SQLite3** – встроенная база данных
- **APScheduler** – планировщик задач
- **aiofiles** – асинхронная работа с файлами

---

## 🚀 Установка и запуск

### Локально (для разработки)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/fliperrsv/telegram_bot.git
   cd telegram_bot
```

2. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Создайте файл config.py и укажите токен:
   ```python
   BOT_TOKEN = "ваш_токен_от_BotFather"
   ADMIN_ID = 123456789  # ваш Telegram ID
   TIMEZONE = "Europe/Moscow"
   ```
5. Запустите бота:
   ```bash
   python bot.py
   ```

На сервере (Ubuntu / Debian)

```bash
# Установка Python и зависимостей
apt update && apt install python3 python3-pip -y
pip install aiogram apscheduler aiofiles pytz

# Создание папки и копирование файлов
mkdir ~/telegram_bot && cd ~/telegram_bot
# (скопируйте файлы через nano или scp)

# Запуск
python3 bot.py

# Для фонового режима
screen -S telegram_bot python3 bot.py
# Отключиться: Ctrl+A, D
# Вернуться: screen -r telegram_bot
```

---

📂 Структура проекта

```
telegram_bot/
├── bot.py              # основной файл (запуск, фоновые задачи)
├── config.py           # токен, ADMIN_ID, TIMEZONE
├── database.py         # работа с SQLite (пользователи, напоминания)
├── handlers.py         # обработчики команд и callback-запросов
├── keyboards.py        # инлайн-клавиатуры
├── scheduler.py        # планировщик задач (APScheduler)
├── requirements.txt    # зависимости
├── users.db            # база данных (создаётся автоматически)
└── README.md           # этот файл
```

---

📋 Команды бота

Команда Описание
/start Приветствие и главное меню
/help Справка по командам
/about Информация о разработчике
/premium Премиум-доступ (заглушка)
/reminders Список напоминаний

---

👑 Администраторские функции

Для администратора (указан ADMIN_ID в config.py) доступны дополнительные возможности:

· /stats – статистика бота (количество пользователей)
· /broadcast – массовая рассылка сообщений всем пользователям

---

🌐 Поддержка языков

Пользователь может выбрать язык:

· 🇷🇺 Русский
· 🇬🇧 English

Язык сохраняется в базе данных.

---

⏰ Напоминания

Пользователь может установить напоминание:

1. Нажать кнопку «Напомнить» в главном меню
2. Выбрать быстрый интервал (1 час, 3 часа, завтра)
3. Или ввести свою дату и время (в разработке)

Бот автоматически отправляет уведомление в указанное время.

---

📦 Примеры кода (ключевые фрагменты)

Инициализация базы данных

```python
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            language TEXT DEFAULT 'ru',
            is_premium INTEGER DEFAULT 0,
            joined_at TIMESTAMP,
            last_active TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
```

Фоновая проверка напоминаний

```python
async def check_reminders():
    while True:
        reminders = get_active_reminders()
        for rem_id, user_id, text, remind_at in reminders:
            await bot.send_message(user_id, f"🔔 Напоминание: {text}")
            mark_reminder_done(rem_id)
        await asyncio.sleep(60)
```

---

📞 Контакты

· Разработчик: Сергей Резунков
· Telegram: @fliperrsv1
· Email: fliperrsv@yandex.ru
· Портфолио: fliperrsv.github.io/portfolio
· GitHub: github.com/fliperrsv

---

📄 Лицензия

Проект создан для демонстрации навыков. Код может использоваться как основа для собственных разработок. Упоминание автора приветствуется.

© 2025 Сергей Резунков

```

---
