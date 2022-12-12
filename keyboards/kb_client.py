from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove 


cmd_kb_client = ReplyKeyboardMarkup(resize_keyboard=True,
                         one_time_keyboard=True)
b_help = KeyboardButton('Помощь')
b_add_event = KeyboardButton('Добавить событие')
b_today = KeyboardButton('Дела сегодня')
b_week = KeyboardButton('Дела на неделе')


cmd_kb_client.add(b_help).insert(b_add_event).add(b_week).insert(b_today)


# start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
# start_kb.row('Navigation Calendar', 'Dialog Calendar')

