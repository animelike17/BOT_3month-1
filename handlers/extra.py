import random

from aiogram import types, Dispatcher
from config import bot, dp, ADMIN



async def echo(message: types.Message):
    if message.text.startswith('game') and message.from_user.id in ADMIN:
        emojis = ['🎯', '🎳', '🎰', '🎲', '⚽️', '🏀']
        dice = random.choice(emojis)
        await bot.send_dice(message.chat.id, emoji=dice)
    elif message.text.isdigit():
        await bot.send_message(message.chat.id, int(message.text) ** 2)
    else:
        await bot.send_message(message.chat.id, message.text)


def register_extra_handlers(dp: Dispatcher):
    dp.register_message_handler(echo)
