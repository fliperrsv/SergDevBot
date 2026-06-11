import asyncio
from aiogram import Bot, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from datetime import datetime, timedelta
from config import ADMIN_ID
from database import add_user, update_last_active, get_user_language, update_language, get_users_count, get_all_users, add_reminder, get_user_reminders
from keyboards import main_keyboard, language_keyboard, reminder_keyboard, admin_keyboard

# Тексты на разных языках
TEXTS = {
    'ru': {
        'welcome': "👋 Привет, {name}!\n\nМеня зовут Сергей Резунков, я веб-разработчик. Создаю сайты и Telegram-ботов под ключ.\n\n➡️ Нажми на кнопки ниже, чтобы узнать больше.",
        'help': "🤖 Доступные команды:\n/start – начать\n/help – помощь\n/about – обо мне\n/premium – премиум\n/reminders – мои напоминания",
        'about': "🔧 Веб-разработчик | Python-разработчик\n\nСтек: HTML5, CSS3, JS, React, Python, aiogram, Flask, Git\n\n📂 Портфолио: fliperrsv.github.io/portfolio",
        'contacts': "📞 Мои контакты:\n\nTelegram: @fliperrsv1\nEmail: fliperrsv@yandex.ru\nGitHub: github.com/fliperrsv",
        'services': "🛠 Услуги:\n\n✅ Лендинг – от 5000 ₽\n✅ Сайт-визитка – от 7000 ₽\n✅ Telegram-бот – от 4000 ₽\n✅ Доработка сайтов",
        'language_changed': "🌐 Язык изменён на русский",
        'reminder_ask': "⏰ Напишите текст напоминания:",
        'reminder_time_ask': "📅 Введите дату и время в формате: ГГГГ-ММ-ДД ЧЧ:ММ\nНапример: 2025-12-31 18:00",
        'reminder_set': "✅ Напоминание установлено на {time}",
        'reminder_notify': "🔔 Напоминание: {text}",
        'no_reminders': "📭 У вас нет активных напоминаний",
        'premium_text': "⭐ Премиум-доступ даёт:\n• Приоритетную поддержку\n• Скидку 10% на услуги\n• Ранний доступ к новым функциям\n\n💰 Стоимость: 199 ₽/мес\n\nДля оформления напишите @fliperrsv1"
    },
    'en': {
        'welcome': "👋 Hello, {name}!\n\nI'm Sergey Rezunkov, web developer. I create websites and Telegram bots.\n\n➡️ Click the buttons below to learn more.",
        'help': "🤖 Available commands:\n/start – start\n/help – help\n/about – about me\n/premium – premium access\n/reminders – my reminders",
        'about': "🔧 Web Developer | Python Developer\n\nStack: HTML5, CSS3, JS, React, Python, aiogram, Flask, Git\n\n📂 Portfolio: fliperrsv.github.io/portfolio",
        'contacts': "📞 My contacts:\n\nTelegram: @fliperrsv1\nEmail: fliperrsv@yandex.ru\nGitHub: github.com/fliperrsv",
        'services': "🛠 Services:\n\n✅ Landing page – from $60\n✅ Business card site – from $80\n✅ Telegram bot – from $50\n✅ Website support",
        'language_changed': "🌐 Language changed to English",
        'reminder_ask': "⏰ Enter reminder text:",
        'reminder_time_ask': "📅 Enter date and time in format: YYYY-MM-DD HH:MM\nExample: 2025-12-31 18:00",
        'reminder_set': "✅ Reminder set for {time}",
        'reminder_notify': "🔔 Reminder: {text}",
        'no_reminders': "📭 You have no active reminders",
        'premium_text': "⭐ Premium access gives:\n• Priority support\n• 10% discount on services\n• Early access to new features\n\n💰 Price: $5/month\n\nContact @fliperrsv1 to subscribe"
    }
}

def get_text(user_id, key):
    lang = get_user_language(user_id)
    return TEXTS.get(lang, TEXTS['ru']).get(key, TEXTS['ru'][key])

async def register_handlers(dp, bot):
    
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        user = message.from_user
        add_user(user.id, user.username, user.first_name, user.last_name)
        lang = get_user_language(user.id)
        await message.answer(get_text(user.id, 'welcome').format(name=user.first_name), reply_markup=main_keyboard(lang))

    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        update_last_active(message.from_user.id)
        await message.answer(get_text(message.from_user.id, 'help'), parse_mode=ParseMode.MARKDOWN)

    @dp.message(Command("about"))
    async def cmd_about(message: types.Message):
        update_last_active(message.from_user.id)
        await message.answer(get_text(message.from_user.id, 'about'), parse_mode=ParseMode.MARKDOWN)

    @dp.message(Command("premium"))
    async def cmd_premium(message: types.Message):
        update_last_active(message.from_user.id)
        await message.answer(get_text(message.from_user.id, 'premium_text'), parse_mode=ParseMode.MARKDOWN)

    @dp.message(Command("reminders"))
    async def cmd_reminders(message: types.Message):
        reminders = get_user_reminders(message.from_user.id)
        if not reminders:
            await message.answer(get_text(message.from_user.id, 'no_reminders'))
        else:
            text = "📋 **Ваши напоминания:**\n\n"
            for r in reminders:
                status = "✅" if r[3] == "done" else "⏳"
                text += f"{status} {r[1]} – до {r[2]}\n"
            await message.answer(text, parse_mode=ParseMode.MARKDOWN)

    @dp.callback_query(F.data == "contacts")
    async def callback_contacts(callback: types.CallbackQuery):
        update_last_active(callback.from_user.id)
        await callback.message.edit_text(get_text(callback.from_user.id, 'contacts'), parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]]))
        await callback.answer()

    @dp.callback_query(F.data == "services")
    async def callback_services(callback: types.CallbackQuery):
        update_last_active(callback.from_user.id)
        await callback.message.edit_text(get_text(callback.from_user.id, 'services'), parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")], [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]]))
        await callback.answer()

    @dp.callback_query(F.data == "language")
    async def callback_language(callback: types.CallbackQuery):
        await callback.message.edit_text("🌐 Выберите язык / Choose language:", reply_markup=language_keyboard())
        await callback.answer()

    @dp.callback_query(F.data.startswith("lang_"))
    async def callback_set_language(callback: types.CallbackQuery):
        lang = callback.data.split("_")[1]
        update_language(callback.from_user.id, lang)
        await callback.message.edit_text(TEXTS[lang]['language_changed'], reply_markup=main_keyboard(lang))
        await callback.answer()

    @dp.callback_query(F.data == "back_to_main")
    async def callback_back_to_main(callback: types.CallbackQuery):
        lang = get_user_language(callback.from_user.id)
        await callback.message.delete()
        user = callback.from_user
        await callback.message.answer(TEXTS[lang]['welcome'].format(name=user.first_name), reply_markup=main_keyboard(lang))

    @dp.callback_query(F.data == "reminder")
    async def callback_reminder(callback: types.CallbackQuery):
        await callback.message.edit_text(get_text(callback.from_user.id, 'reminder_ask'), reply_markup=reminder_keyboard())
        await callback.answer()

    @dp.callback_query(F.data.startswith("remind_"))
    async def callback_set_quick_reminder(callback: types.CallbackQuery):
        action = callback.data.split("_")[1]
        now = datetime.now()
        if action == "1h":
            remind_at = now + timedelta(hours=1)
        elif action == "3h":
            remind_at = now + timedelta(hours=3)
        elif action == "tomorrow":
            remind_at = now + timedelta(days=1)
        else:
            await callback.message.edit_text("✏️ В разработке. Используйте /reminders", reply_markup=main_keyboard(get_user_language(callback.from_user.id)))
            await callback.answer()
            return
        
        # Сохраняем временное напоминание (без текста – запросим отдельно)
        dp["temp_reminder_time"] = remind_at
        await callback.message.edit_text("📝 Напишите текст напоминания:")
        await callback.answer()

    # Здесь можно добавить обработчики для администратора (статистика, рассылка)
