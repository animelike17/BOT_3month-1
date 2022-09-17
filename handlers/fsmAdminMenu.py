from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMIN

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
        await state.finish()
    else:
        await message.answer('Вводи цифры')





def register_handlers_FSMAdmin(dp: Dispatcher):
    dp.register_message_handler(start, commands='menu')
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_desk, state=FSMAdmin.desk)
    dp.register_message_handler(load_price, state= FSMAdmin.price)

