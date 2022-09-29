import random
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot, dp
from database.bot_dp import sql_command_random
from handlers import news

async def mem(message: types.Message):
    photo = open('media/mem.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo=photo)

async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton('Next', callback_data='button_1')
    markup.add(button_1)
    question = 'Сколько лет Geektech'
    answer = [
        '4',
        '3',
        '7'
    ]

    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answer,
        type='quiz',
        is_anonymous=True,
        correct_option_id=0,
        explanation='больше 3 лет',
        reply_markup =markup
    )

async def pin(message: types.Message):
    if message.reply_to_message:
        await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    else:
        await message.reply('Надо ответить на сообщение')


async def show_random_food(message: types.Message):
    await sql_command_random(message)


async def parser_news(message: types.Message):
    data = news.parser()[:3]
    for item in data:
        await bot.send_message(message.from_user.id,
                               f"{item['time']}\n"
                               f"{item['title']}\n"
                               f"{item['link']}")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(mem, commands=['mem'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!')
    dp.register_message_handler(show_random_food, commands=['random'])
    dp.register_message_handler(parser_news, commands=['news'])



