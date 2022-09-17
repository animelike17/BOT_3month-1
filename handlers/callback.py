from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot, dp

async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_2 = InlineKeyboardButton('Next', callback_data='button_2')
    markup.add(button_2)
    question = 'Сколько лет Geektech'
    answer = [
        '4',
        '3',
        '7'
    ]

    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answer,
        type='quiz',
        is_anonymous=True,
        correct_option_id=0,
        explanation='больше 3 лет',
        reply_markup =markup
    )


async def quiz_3(call: types.CallbackQuery):
    question = 'Сколько лет Geektech'
    answer = [
        '4',
        '3',
        '7'
    ]

    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answer,
        type='quiz',
        is_anonymous=True,
        correct_option_id=0,
        explanation='больше 3 лет'
    )


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, lambda call: call.data =='button_1')
    dp.register_callback_query_handler(quiz_3, lambda call: call.data =='button_2' )
