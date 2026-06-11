from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def main_keyboard(lang='ru'):
    if lang == 'ru':
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")],
            [InlineKeyboardButton(text="🛠 Услуги", callback_data="services")],
            [InlineKeyboardButton(text="📂 Портфолио", url="https://fliperrsv.github.io/portfolio/")],
            [InlineKeyboardButton(text="⭐ Отзывы", callback_data="reviews")],
            [InlineKeyboardButton(text="⏰ Напомнить", callback_data="reminder")],
            [InlineKeyboardButton(text="🌐 Язык", callback_data="language")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Contacts", callback_data="contacts")],
            [InlineKeyboardButton(text="🛠 Services", callback_data="services")],
            [InlineKeyboardButton(text="📂 Portfolio", url="https://fliperrsv.github.io/portfolio/")],
            [InlineKeyboardButton(text="⭐ Reviews", callback_data="reviews")],
            [InlineKeyboardButton(text="⏰ Remind me", callback_data="reminder")],
            [InlineKeyboardButton(text="🌐 Language", callback_data="language")]
        ])

def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
    ])

def reminder_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🕐 Через 1 час", callback_data="remind_1h")],
        [InlineKeyboardButton(text="🕒 Через 3 часа", callback_data="remind_3h")],
        [InlineKeyboardButton(text="📅 На завтра", callback_data="remind_tomorrow")],
        [InlineKeyboardButton(text="✏️ Своя дата", callback_data="remind_custom")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ])

def admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton(text="⭐ Premium", callback_data="admin_premium")]
    ])
