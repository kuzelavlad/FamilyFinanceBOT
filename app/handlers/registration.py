import string

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types

from bot_creation import bot
from bot_keyboard import start
from services.bot_service import app_serv
from states.bot_states import RegistationState
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from bot_creation import bot
from states.bot_states import RegistationState
import pprint



DELETE_MESSAGE_KEY = "msg_to_delete"



async def type_help_message(text: str, msg: types.Message, state: FSMContext):
    message = await msg.answer(text)
    await state.update_data({DELETE_MESSAGE_KEY: message})

async def delete_help_message(state: FSMContext):
    state_data = await state.get_data()
    await state_data["msg_to_delete"].delete()






async def registration(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RegistationState.username.state)
    await callback.message.delete()
    await type_help_message("Введите Ваше Имя", callback.message, state)


async def get_username(msg: types.Message, state: FSMContext):
    await delete_help_message(state)
    await state.update_data(username=msg.text)
    await msg.delete()
    await state.set_state(RegistationState.password.state)
    await type_help_message("Введите пароль: ", msg, state)

async def get_password_1(msg: types.Message, state: FSMContext):
    digits = string.digits
    letters = string.ascii_letters
    acceptable = digits + letters

    if len(str(msg.text)) >= 6 and all([char in acceptable for char in msg.text]) and any([char in digits for char in msg.text]) and any([char in letters for char in msg.text]):
        await delete_help_message(state)
        await state.update_data(password=msg.text)
        await msg.delete()
        # await state.set_state(RegistationState.mail.state)
        await msg.answer("Регистрация прошла успешно \nВыполните вход", reply_markup=start())
        user_data = await state.get_data()
        user_response = app_serv.create_user(user_data)

        response_data = {

            "username": user_data["username"],
            "password": user_data["password"]
        }

        print(response_data)

        await state.finish()
        # await type_help_message("Введите email: ", msg, state)
    else:
        await msg.answer("Пароль должен содержать больше 6 символов: ")
#





# async def get_mail(msg: types.Message, state: FSMContext):
#     if '@' and '.' in msg.text:
#         await delete_help_message(state)
#         await state.update_data(email=msg.text)
#         await msg.delete()
#         await msg.answer("Регистрация прошла успешно \nВыполните вход", reply_markup=start())
#         user_data = await state.get_data()
#         user_response = app_serv.create_user(user_data)
#         await state.finish()
#
#     else:
#         await msg.answer("Введите данные корректно")




def setup_app(dp: Dispatcher):
    dp.register_callback_query_handler(registration, Text(contains="registration"))
    dp.register_message_handler(get_username, state=RegistationState.username)
    dp.register_message_handler(get_password_1, state=RegistationState.password)
    # dp.register_message_handler(get_mail, state=RegistationState.mail)


