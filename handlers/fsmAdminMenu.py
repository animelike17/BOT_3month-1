from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import bot, ADMIN
from database.bot_dp import sql_command_insert, sql_command_delete, sql_command_all

class FSMAdmin(StatesGroup):
    photo=State()
    name=State()
    desk=State()
    price=State()


async  def start(message: types.Message):
    if message.chat.type == 'private' and message.from_user.id in ADMIN:
        await FSMAdmin.photo.set()
        await message.answer(f'привет {message.from_user.full_name} \n'
                             f'Отправь фото ')
    else:
        await  message.answer('ПИши в лс')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer('Придумай название блюда')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer('Опиши блюдо')


async def load_desk(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desk'] = message.text
    await FSMAdmin.next()
    await message.answer('Напиши цену блюда')


async def load_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['price'] = int(message.text)
            await bot.send_photo(message.chat.id, photo=data['photo'],
                                 caption=f"Name: {data['name']} \n"
                                         f"{data['desk']} \n"
                                         f"Price: {data['price']}")
        await sql_command_insert(state)
        await state.finish()
    else:
        await message.answer('Вводи цифры')


async def delete_data(message: types.Message):
    foods = await sql_command_all()
    for food in foods:
        markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton(f'Delete {food[1]}', callback_data=f'Delete {food[1]}')
        markup.add(button)
        await bot.send_photo(message.from_user.id, food[0],
                             caption=f"Name: {food[1]}\n"
                                     f"Description: {food[2]}\n"
                                     f"Price: {food[3]}\n",
                             reply_markup=markup)


async def complete_delete(call: types.CallbackQuery):
    await sql_command_delete(call.data.replace("Delete ", ""))
    await call.answer(text="Стёрт с бд", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("Ну и пошел ты!")

def register_handlers_FSMAdmin(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, commands=['stop'], state='*')
    dp.register_message_handler(cancel_registration,
                                Text(equals='stop', ignore_case=True), state="*")

    dp.register_message_handler(start, commands='menu')
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_desk, state=FSMAdmin.desk)
    dp.register_message_handler(load_price, state= FSMAdmin.price)

    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_callback_query_handler(complete_delete, lambda call: call.data.startswith('Delete '))