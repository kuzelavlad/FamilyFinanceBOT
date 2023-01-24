import json
import logging
import pathlib

from aiogram import Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from handlers.registration import setup_app as registration_user
from handlers.login import setup as login_user, USER_MAPPER
from handlers.main_menu import setup_menu as menu
from bot_creation import bot
from bot_keyboard import *
from services import bot_service

logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot, storage=MemoryStorage())
BACKUP_FILE = "user_backup.json"

async def startup(_):
    bot_service.check_availability()

@dp.message_handler(commands=['start'])
async def startup(message: types.Message):
    inline_kb = start()
    await message.delete()
    await message.answer(f"Добро пожаловать! \nВыберите действия из списка ниже", reply_markup=inline_kb)

@dp.callback_query_handler(Text(contains="exit"), state="*")
async def exit_handler(callback: types.CallbackQuery, state: FSMContext):

    await startup(callback.message)
    await state.finish()
    await callback.answer("Exit pressed")

@dp.callback_query_handler(Text(contains="return"), state="*")
async def return_handler(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await callback.message.answer("Выберите нужную категорию", reply_markup=main_menu_keyboard())
    await state.finish()


registration_user(dp)
login_user(dp)
menu(dp)


async def startup_backup_load(_):
    if pathlib.Path(BACKUP_FILE).exists():
        with open(BACKUP_FILE) as f:
            USER_MAPPER.update(json.load(f))

async def shutdown_backup(_):
    with open(BACKUP_FILE, "w") as f:
        json.dump(USER_MAPPER, f)


executor.start_polling(dp, skip_updates=True, on_startup=startup_backup_load, on_shutdown=shutdown_backup)

