from bot_keyboard import main_menu_keyboard
from services.bot_service import app_serv
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from states.bot_states import LoginState

USER_MAPPER = {}

DELETE_MESSAGE_KEY = "msg_to_delete"


async def type_help_message(text: str, msg: types.Message, state: FSMContext):
    message = await msg.answer(text)
    await state.update_data({DELETE_MESSAGE_KEY: message})

async def delete_help_message(state: FSMContext):
    state_data = await state.get_data()
    await state_data["msg_to_delete"].delete()


async def login(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LoginState.username.state)
    await callback.message.delete()
    await type_help_message("Введите Ваше Имя", callback.message, state)


async def login_username(msg: types.Message, state: FSMContext):
    await delete_help_message(state)
    await state.update_data(username=msg.text)
    await msg.delete()
    await state.set_state(LoginState.password.state)
    await type_help_message("Введите пароль: ", msg, state)


async def login_password(msg: types.Message, state: FSMContext):
    await delete_help_message(state)
    await msg.delete()
    await state.update_data(password=msg.text)
    authorization_data = await state.get_data()

    try:
        user = app_serv.authorization(authorization_data)
        USER_MAPPER[msg.from_user.id] = user

    except:
        await msg.answer("Неверный логин или пароль, попробуйте еще раз")
        await state.set_state(LoginState.username.state)
        await type_help_message("Введите ваше Имя", msg, state)
        raise

    await msg.answer(f"Добро пожаловать! Выберите нужную категорию ", reply_markup=main_menu_keyboard())
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(login, Text(contains="login"))
    dp.register_message_handler(login_username, state=LoginState.username)
    dp.register_message_handler(login_password, state=LoginState.password)
