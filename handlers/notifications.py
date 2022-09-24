import asyncio
import aioschedule
from aiogram import types, Dispatcher
from config import bot


async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = message.from_user.id
    await bot.send_message(chat_id=chat_id, text='ok!')


async def go_to_sleep():
    bot.send_message(chat_id=chat_id, text='Опять понедельник')


async def scheduler():
    aioschedule.every().monday.at("6:00").do(go_to_sleep)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


def register_handlers_notifications(dp: Dispatcher):
    dp.register_message_handler(get_chat_id,
                                lambda word: 'Напомни' in word.text)
