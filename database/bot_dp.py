import random
import sqlite3

from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print('База данных подключена')
    # db.execute('DROP TABLE IF EXISTS menu')
    db.execute("CREATE TABLE IF NOT EXISTS menu "
               "(photo TEXT, "
               "name TEXT PRIMARY KEY, "
               "desk TEXT, "
               "price INTEGER)")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO menu VALUES (?, ?, ?, ?)", tuple(data.values()))
    db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM menu").fetchall()
    random_food = random.choice(result)
    await bot.send_photo(message.from_user.id, random_food[0],
                         caption=f"Name: {random_food[1]}\n"
                                 f"Description: {random_food[2]}\n"
                                 f"Price: {random_food[3]}")


async def sql_command_all():
    return cursor.execute("SELECT * FROM menu").fetchall()


async def sql_command_delete(name):
    cursor.execute("DELETE FROM menu WHERE name == ?", (name,))
    db.commit()
