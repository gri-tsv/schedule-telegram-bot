from datetime import date, datetime, timedelta
import sqlite3 as sq
from create_bot import bot
from aiogram.types import Message


def sql_start():
    global base, db_cur
    base = sq.connect('SheduleMainBot.db')
    db_cur = base.cursor()
    if base:
        print('Database connected, good !')
    base.execute(
        'CREATE TABLE IF NOT EXISTS SheduleMainBot(id INTEGER PRIMARY KEY AUTOINCREMENT, \
        event_user_firstname TEXT, event_date TEXT, event_time TEXT, event_desc TEXT, event_who TEXT )')
    base.commit()


async def cmd_sql_add(state):
    async with state.proxy() as data:
        db_cur.execute('INSERT INTO SheduleMainBot(event_user_firstname, event_date, event_time, event_desc , '
                       'event_who) VALUES (?, ?, ?, ?, ?)',
                       tuple(data.values()))
        base.commit()


async def cmd_sql_read(message):
    for ret in db_cur.execute('SELECT * FROM SheduleMainBot').fetchall():
        await bot.send_message(message.from_user.id,
                               f'{ret[4]}\n{ret[2]}.\nВ {ret[3]}.\nНужны: {ret[5]}.\nДобавил - {ret[1]}.')


async def cmd_sql_read_today(message):
    for ret in db_cur.execute("SELECT * FROM SheduleMainBot WHERE strftime('%d', event_date) = strftime('%d','now') GROUP BY event_time ORDER BY event_date ").fetchall():
        date_from_db = ret[2]
        valid_date = datetime.strptime(date_from_db, '%Y-%m-%d')
        valid_date_event = datetime.date(valid_date).strftime('%d.%m.%Y')
        time_from_db = ret[3]
        valid_time = datetime.strptime(time_from_db, '%H.%M')
        valid_time_event = datetime.time(valid_time).strftime('%H.%M')
        await bot.send_message(message.from_user.id,
                               f'{ret[4]}\n{valid_date_event}.\nВ {valid_time_event}.\nНужны: {ret[5]}.\nДобавил - {ret[1]}.')
        print(valid_date_event)

async def cmd_sql_read_week(message):
    for ret in db_cur.execute("SELECT * FROM SheduleMainBot WHERE strftime('%W',event_date) = strftime('%W','now') GROUP BY event_time ORDER BY event_date").fetchall():
        date_from_db = ret[2]
        valid_date = datetime.strptime(date_from_db, '%Y-%m-%d')
        valid_date_event = datetime.date(valid_date).strftime('%d.%m.%Y')
        time_from_db = ret[3]
        valid_time = datetime.strptime(time_from_db, '%H.%M')
        valid_time_event = datetime.time(valid_time).strftime('%H.%M')
        await bot.send_message(message.from_user.id,
                               f'{ret[4]}\n{valid_date_event}.\nВ {valid_time_event}.\nНужны: {ret[5]}.\nДобавил - {ret[1]}.')
        print(valid_time_event)

# last insert event
# async def cmd_sql_read_last(message):
#     for ret in db_cur.execute(
#             'SELECT * FROM SheduleMainBot WHERE id =(SELECT last_insert_rowid() FROM SheduleMainBot)'):
#         await bot.send_message(
#             message.from_user.id,f'{ret[4]}\n{ret[2]}.\nВ {ret[3]}.\nНужны: {ret[5]}.\nДобавил - {ret[1]}.'
#         )

# async def cmd_list_today(message):
