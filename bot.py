import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import init_db, get_active_reminders, mark_reminder_done
from handlers import register_handlers
from scheduler import start_scheduler
from aiogram.types import BotCommand

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def set_commands():
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="about", description="О разработчике"),
        BotCommand(command="premium", description="Премиум-доступ"),
        BotCommand(command="reminders", description="Мои напоминания"),
    ]
    await bot.set_my_commands(commands)

async def check_reminders():
    """Фоновая задача для проверки напоминаний"""
    while True:
        reminders = get_active_reminders()
        for rem_id, user_id, text, remind_at in reminders:
            try:
                await bot.send_message(user_id, f"🔔 Напоминание: {text}")
                mark_reminder_done(rem_id)
            except Exception as e:
                logging.error(f"Reminder error for {user_id}: {e}")
        await asyncio.sleep(60)

async def main():
    init_db()
    await set_commands()
    await register_handlers(dp, bot)
    asyncio.create_task(check_reminders())
    start_scheduler(bot)
    logging.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
