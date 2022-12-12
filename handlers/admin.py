from datetime import date, time

from aiogram import types, Dispatcher
from create_bot import dp, bot

from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


# States
class FSMAddEvent(StatesGroup):
    date = State()  # Will be represented in storage as 'FSMAddEvent:date'
    time = State()  # Will be represented in storage as 'FSMAddEvent:time'
    desc = State()  # Will be represented in storage as 'FSMAddEvent:desc'
    who = State()  # Will be represented in storage as 'FSMAddEvent:who_haveto_be'


# начало диалога добавления события
# @dp.message_handler(commands=['/add_event', 'Добавить событие'], state=None)
async def fsm_add_event(message: types.Message):
    await FSMAddEvent.date.set()
    await message.reply("Запись события началась,\nдля отмены пишите 'отмена' или 'cancel'.\nВыберите дату: ")


# ловим первый ответ и пишем в словарь
# @dp.message_handler(content_types=['date'], state=FSMAddEvent.date)
async def fsm_add_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Дата'] = date(message.text)
    await FSMAddEvent.next()
    await message.reply("В какое время?")


# добавляем время
# @dp.message_handler(content_types=['time'], state=FSMAddEvent.time)
async def fsm_add_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Время'] = time(message.text)
    await FSMAddEvent.next()
    await message.reply("Теперь напишите описание к событию: ")


# добавляем описание к событию
# @dp.message_handler(state=FSMAddEvent.desc)
async def fsm_add_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Описание'] = message.text
    await FSMAddEvent.next()
    await message.reply('Кто должен присутствовать? (через запятую)')


# добавляем присутствующих и завершаем
# @dp.message_handler(state=FSMAddEvent.who_haveto_be)
async def fsm_add_who(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Кто'] = message.text

    async with state.proxy() as data:
        await message.answer(str(data))
    await state.finish()


# выход из состояний
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def fsm_cancel(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(fsm_add_event, commands=['Добавить событие', 'add_event'], state=None)
    dp.register_message_handler(fsm_add_date, content_types=['date'], state=FSMAddEvent.date)
    dp.register_message_handler(fsm_add_time, content_types=['time'], state=FSMAddEvent.time)
    dp.register_message_handler(fsm_add_desc, state=FSMAddEvent.desc)
    dp.register_message_handler(fsm_add_who, state=FSMAddEvent.who)
    dp.register_message_handler(fsm_cancel, state="*", commands='отмена')
    dp.register_message_handler(fsm_cancel, Text(equals='отмена', ignore_case=True), state='*')


