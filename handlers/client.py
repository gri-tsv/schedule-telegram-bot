import types
from datetime import date, time

from aiogram import Dispatcher,types
from aiogram.types import Message, CallbackQuery
from create_bot import dp, bot

from aiogram.dispatcher.filters import Text
from keyboards.kb_client import cmd_kb_client


LIST_COMMANDS = """
/start - начать работу с ботом
/help - список команд
/add_event - добавить событие
/today_event - список дел на сегодня
/week_event - список дел на неделю
"""

LIST_EVENTS = {}


# starting bot when user sends `/start` command, answering with inline calendar
@dp.message_handler(Text(equals=['start', 'старт']))
async def cmd_start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=cmd_kb_client)
    await message.delete()
    # Set state()
    # await Form.username.set()


@dp.message_handler(Text(equals=['Помощь', 'help']))
async def cmd_help(message: Message):
    await message.answer(text=LIST_COMMANDS)
    # await message.delete()


@dp.message_handler(Text(equals=['today_event', 'Дела на сегодня']))
async def cmd_today_event(message: Message):
    await message.answer("Список дел на сегодня: ")


@dp.message_handler(Text(equals=['week_event', 'Дела на неделю']))
async def cmd_week_event(message: Message):
    await message.answer("Список дел на неделю: ")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_help, commands=['help'])
    dp.register_message_handler(cmd_today_event, commands=['today_event', 'Дела на сегодня'])
    dp.register_message_handler(cmd_week_event, commands=['week_event', 'Дела на неделю'])