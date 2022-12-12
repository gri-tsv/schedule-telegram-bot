# - *- coding: utf- 8 - *-
import logging
from datetime import datetime

from aiogram.utils import executor
# from handlers import client, admin, other

from aiogram import types
from aiogram.types import Message, CallbackQuery
from create_bot import bot, dp
from aiogram.dispatcher.filters import Text
from keyboards import kb_client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
# from database.mysql_db import mysql_start, cmd_mysql_add, cmd_mysql_read, cmd_mysql_read_last
from database.sqlite_db import sql_start, cmd_sql_add, cmd_sql_read, cmd_sql_read_today, cmd_sql_read_week #, cmd_sql_read_last
from aiogram_calendar import simple_cal_callback, SimpleCalendar

# Configure logging
logging.basicConfig(level=logging.INFO)
# event_add_number_id_for_db = 1
# client.register_handlers_client(dp)
# admin.register_handlers_admin(dp)

#####################################################################################
#                           CLIENT
LIST_COMMANDS = """
/start - начать работу с ботом
/help - список команд
/add_event - добавить событие
/today_event - список дел на сегодня
/week_event - список дел на неделю
"""
# LIST_COMMANDS = """
# /start - начать работу с ботом
# /help - кнопка Помощь - список команд
# /add_event - кнопка Добавить событие- добавить событие
# /today_event - кнопка Дела сегодня - список дел на сегодня
# /week_event - кнопка Дела на неделе - список дел на неделю
# """


# starting bot when user sends `/start` command, answering with inline calendar
@dp.message_handler(Text(equals=['/start', 'старт']))
async def cmd_start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=kb_client.cmd_kb_client)
    # await message.delete()


@dp.message_handler(Text(equals=['Помощь', '/help']))
async def cmd_help(message: Message):
    await message.reply(text=LIST_COMMANDS, reply_markup=kb_client.cmd_kb_client)


@dp.message_handler(Text(equals=['/today_event', 'Дела сегодня']))
async def cmd_today_event(message: Message):
    await message.answer("Список дел на сегодня: ", reply_markup=kb_client.cmd_kb_client)
    await cmd_sql_read_today(message)


@dp.message_handler(Text(equals=['/week_event', 'Дела на неделе']))
async def cmd_week_event(message: Message):
    await message.answer("Список дел на неделю: ", reply_markup=kb_client.cmd_kb_client)
    await cmd_sql_read_week(message)


# def register_handlers_client(dp: Dispatcher):
#     dp.register_message_handler(cmd_start, commands=['start'])
#     dp.register_message_handler(cmd_help, commands=['help'])
#     dp.register_message_handler(cmd_today_event, commands=['today_event', 'Дела на сегодня'])
#     dp.register_message_handler(cmd_week_event, commands=['week_event', 'Дела на неделю'])


#################################################################################################################
#                                   ADMIN
# States
class FSMAddEvent(StatesGroup):
    event_firstname_and_date = State()
    event_date = State()  # Will be represented in storage as 'FSMAddEvent:date'
    event_time = State()  # Will be represented in storage as 'FSMAddEvent:time'
    event_desc = State()  # Will be represented in storage as 'FSMAddEvent:desc'
    event_who = State()  # Will be represented in storage as 'FSMAddEvent:who_haveto_be'


# начало диалога добавления события
@dp.message_handler(Text(equals=['/add_event', 'Добавить событие']), State=None)
async def fsm_add_event(message: types.Message):
    await FSMAddEvent.event_firstname_and_date.set()
    await message.answer("Запись события началась,\nдля отмены пишите 'отмена' или 'cancel'.")
    await message.answer("Напишите дату в формате дд.мм.гг : ")
    # await message.answer("Напишите дату в формате гггг-мм-дд: ") # , reply_markup=await SimpleCalendar().start_calendar()


# выход из состояний
@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def fsm_cancel(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Запись отменена.', reply_markup=kb_client.cmd_kb_client)


# ловим первый ответ и пишем в словарь
# @dp.callback_query_handler(simple_cal_callback.filter(), state=FSMAddEvent.event_firstname_and_date)
@dp.message_handler(state=FSMAddEvent.event_firstname_and_date)
async def fsm_add_date(message: types.Message, state: FSMContext):
    try:
        # async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
        #     selected, date_calendar_selected = await SimpleCalendar().process_selection(callback_query, callback_data)
        #     if selected:
        #         await callback_query.message.answer(
        #             f'You selected {date_calendar_selected.strftime("%d.%m.%Y")}',
        #             reply_markup=kb_client.cmd_kb_client
        #         )
        #     valid_date_event_from_calendar = date_calendar_selected.strftime("%d.%m.%Y")
        date_event_str = message.text
        date_for_sql = datetime.strptime(date_event_str, '%d.%m.%y').date().strftime('%d.%m.%y')

        async with state.proxy() as data:
            data['event_user_firstname'] = message.from_user.first_name
        await FSMAddEvent.next()

        async with state.proxy() as data:
            data['event_date'] = date_for_sql
        await FSMAddEvent.next()

        await message.answer("В какое время?\nВведите в формате чч.мм :")
    except ValueError:
        await message.reply('Неправильный формат даты.\nПопробуйте еще раз.')


# добавляем время
@dp.message_handler(state=FSMAddEvent.event_time)
async def fsm_add_time(message: types.Message, state: FSMContext):
    try:
        time_event_str = message.text
        valid_time_event = datetime.strptime(time_event_str, '%H.%M').time()

        async with state.proxy() as data:
            data['event_time'] = valid_time_event
        await FSMAddEvent.next()
        await message.answer("Теперь напишите описание к событию: ")
    except ValueError:
        await message.reply('Неправильный формат времени.\nПопробуйте еще раз.')


# добавляем описание к событию
@dp.message_handler(state=FSMAddEvent.event_desc)
async def fsm_add_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_desc'] = message.text
    await FSMAddEvent.next()
    await message.answer('Кто должен присутствовать? (через запятую)')


# добавляем присутствующих и завершаем
@dp.message_handler(state=FSMAddEvent.event_who)
async def fsm_add_who(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['event_who'] = message.text
    await FSMAddEvent.next()
    await message.answer("Событие добавлено.", reply_markup=kb_client.cmd_kb_client)
    # await cmd_sql_read_last(message)
    await cmd_sql_add(state)
    await state.finish()


# def register_handlers_admin(dp: Dispatcher):
#     dp.register_message_handler(fsm_add_event, commands=['Добавить событие', 'add_event'], state=None)
#     dp.register_message_handler(fsm_cancel, state="*", commands='отмена')
#     dp.register_message_handler(fsm_cancel, Text(equals='отмена', ignore_case=True), state='*')
#     dp.register_message_handler(fsm_add_date, content_types=['date'], state=FSMAddEvent.date)
#     dp.register_message_handler(fsm_add_time, content_types=['time'], state=FSMAddEvent.time)
#     dp.register_message_handler(fsm_add_desc, state=FSMAddEvent.desc)
#     dp.register_message_handler(fsm_add_who, state=FSMAddEvent.who)


@dp.message_handler()
async def empty(message: types.Message):
    await message.answer('Не понимаю вас.\nВот список доступных команд: ')
    await message.answer(text=LIST_COMMANDS, reply_markup=kb_client.cmd_kb_client)
    await message.delete()


async def on_startup(_):
    print("Bot started")
    sql_start()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
