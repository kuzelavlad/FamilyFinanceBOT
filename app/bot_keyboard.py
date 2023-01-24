from aiogram import Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

from services.bot_service import app_serv


def start():

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Log IN", callback_data="login"))
    inline_kb.add(types.InlineKeyboardButton("Registration", callback_data="registration"))


    return inline_kb

def main_menu_keyboard():
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Доходы", callback_data="earnings"))
    inline_kb.add(types.InlineKeyboardButton("Расходы", callback_data="expenses"))
    # inline_kb.add(types.InlineKeyboardButton("Копилка", callback_data="money_box"))
    inline_kb.add(types.InlineKeyboardButton("Отчет", callback_data="report"))
    inline_kb.add(types.InlineKeyboardButton("Выход", callback_data="exit"))


    return inline_kb


def currency_keyboard():

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    currency_data = app_serv.get_currencies()
    for currency in currency_data:
        inline_kb.add(types.InlineKeyboardButton(currency["short_name"], callback_data=f"currency_{currency['id']}"))
    return inline_kb






def generate_category_inline(is_earning: bool = True):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    categories_data = app_serv.get_categories(is_earning)
    for category in categories_data:
        inline_kb.add(types.InlineKeyboardButton(category["title"], callback_data=f"category_{category['id']}"))
    return inline_kb


def money_box_main():

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Текущие цели", callback_data="current_goals"))
    inline_kb.add(types.InlineKeyboardButton("Добавить новую", callback_data="add_new"))
    inline_kb.add(types.InlineKeyboardButton("Назад", callback_data="return"))


    return inline_kb



def return_button():



    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Назад", callback_data="return"))

    return inline_kb


