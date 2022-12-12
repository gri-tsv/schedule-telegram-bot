from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b_admin_today = KeyboardButton('Дела сегодня')
b_admin_week = KeyboardButton('Дела на неделе')

cmd_kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(b_admin_today).add(b_admin_week)

