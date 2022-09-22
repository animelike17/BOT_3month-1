from aiogram.utils import executor

from config import dp, bot
import logging
import asyncio

from handlers import client, extra, callback, admin, fsmAdminMenu
from database.bot_dp import sql_create

async def on_startup(_):
    sql_create()

client.register_handlers_client(dp)
fsmAdminMenu.register_handlers_FSMAdmin(dp)
callback.register_callback_handlers(dp)
# admin.register_handlers_admin(dp)/
extra.register_extra_handlers(dp)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
