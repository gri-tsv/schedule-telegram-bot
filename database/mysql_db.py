from create_bot import bot
from aiogram.types import Message
from getpass import getpass
from mysql.connector import connect, Error

mysql_connect_config = {
  'user': 'grITsv',
  'password': 'rt45ui78',
  'host': 'grITsv.mysql.pythonanywhere-services.com',
  'database': 'grITsv$ScheduleTgBot',
  'raise_on_warnings': True
}

def mysql_start():
    global base, db_cur
    try:
        with connect(**mysql_connect_config) as connection:
            print(connection)

        with connection.cursor() as cursor:

            cursor.execute(
                'CREATE TABLE IF NOT EXISTS SheduleMainBot(id INTEGER PRIMARY KEY AUTO_INCREMENT, \
                event_user_firstname TEXT, event_date TEXT, event_time TEXT, event_desc TEXT, event_who TEXT )')
            base.commit()
    except Error as e:
        print(e)
    # base = mysql.connector.connect()
    # db_cur = base.cursor()


async def cmd_mysql_add(state):
    async with state.proxy() as data:
        db_cur.execute('INSERT INTO SheduleMainBot(event_user_firstname, event_date, event_time, event_desc , '
                       'event_who) VALUES (?, ?, ?, ?, ?)',
                       tuple(data.values()))
        base.commit()


async def cmd_mysql_read(message):
    for ret in db_cur.execute('SELECT * FROM SheduleMainBot').fetchall():
        await bot.send_message(message.from_user.id,
                               f'{ret[4]}\n{ret[2]}.\nВ {ret[3]}.\nНужны: {ret[5]}.\nДобавил - {ret[1]}.')


async def cmd_mysql_read_last(message):
    for ret in db_cur.execute(
            'SELECT * FROM SheduleMainBot AS STB \
            WHERE id =(SELECT MAX(id) FROM SheduleMainBot AS STB2 \
            WHERE STB.id = STB2.id) ORDER BY STB.id'):
        await bot.send_message(
            message.from_user.id,
            f'{ret[4]}\n{ret[2]}.\nВ {ret[3]}.\nНужны: {ret[5]}.\nДобавил - {ret[1]}.'
        )

# async def cmd_list_today(message):


