from bot_keyboard import main_menu_keyboard, generate_category_inline
from handlers.login import USER_MAPPER
from services.bot_service import app_serv
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from states.bot_states import MenuEarningState, MenuExpensesState, MoneyBoxState
from bot_keyboard import currency_keyboard, money_box_main, return_button

DELETE_MESSAGE_KEY = "msg_to_delete"


async def type_help_message(text: str, msg: types.Message, state: FSMContext):
    message = await msg.answer(text)
    await state.update_data({DELETE_MESSAGE_KEY: message})

async def delete_help_message(state: FSMContext):
    state_data = await state.get_data()
    await state_data["msg_to_delete"].delete()





async def earnings(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MenuEarningState.amount.state)
    await callback.message.delete()
    await type_help_message("Введите сумму статьи доходов ", callback.message, state)


async def amount_earnings(msg: types.Message, state: FSMContext):
    summa = msg.text

    if summa.isdigit():

        await msg.delete()
        await state.update_data(amount=msg.text)
        await state.set_state(MenuEarningState.currency.state)
        # await msg.delete()
        await msg.answer("Выберите Валюту", reply_markup=currency_keyboard())
    else:
        await msg.answer("Введите корректные данные")



async def category_earnings(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(currency=callback.data.split("_")[-1])
    await state.set_state(MenuEarningState.category.state)
    await callback.message.answer("Выберите нужную категорию", reply_markup=generate_category_inline())


async def finish_earnings(callback: types.CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split("_")[-1])  # category_1
    state_data = await state.get_data()
    app_serv.create_transaction({**state_data, "category": category_id, "is_earing": True, "user": USER_MAPPER[callback.from_user.id]["id"]})
    await callback.message.delete()
    await state.finish()
    await callback.message.answer("Данные внесены успешно. Выберите нужную категорию ", reply_markup=main_menu_keyboard())









async def expenses(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MenuExpensesState.amount.state)
    await callback.message.delete()
    await callback.message.answer("Введите сумму статьи расходов")

async def amount_expenses(msg: types.Message, state: FSMContext):
    summa = msg.text

    if summa.isdigit():
        await msg.delete()
        await state.update_data(amount=msg.text)
        await state.set_state(MenuExpensesState.currency.state)
        # await msg.delete()
        await msg.answer("Выберите Валюту", reply_markup=currency_keyboard())
    else:
        await msg.answer("Введите корректные данные")


async def currency_expenses(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(currency=callback.data.split("_")[-1])
    await state.set_state(MenuExpensesState.category.state)
    await callback.message.answer("Выберите категорию статьи расходов ", reply_markup=generate_category_inline(is_earning=False))


async def finish_expenses(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    app_serv.create_transaction({**state_data, "category": callback.data.split("_")[-1], "is_earning": False, "user": USER_MAPPER[callback.from_user.id]["id"]})
    await callback.message.delete()
    await state.finish()
    await callback.message.answer("Данные внесены успешно. Выберите нужную категорию ", reply_markup=main_menu_keyboard())









async def money_box(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(MoneyBoxState.current_goals.state)
    await callback.message.answer("Выберите нужную категорию", reply_markup=money_box_main())

async def current_goals_box(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data()


def setup_menu(dp: Dispatcher):
    dp.register_callback_query_handler(earnings, Text(equals="earnings"))
    dp.register_message_handler(amount_earnings, state=MenuEarningState.amount)
    dp.register_callback_query_handler(category_earnings, state=MenuEarningState.currency)
    dp.register_callback_query_handler(finish_earnings, state=MenuEarningState.category)
    dp.register_callback_query_handler(expenses, Text(equals="expenses"))
    dp.register_message_handler(amount_expenses, state=MenuExpensesState.amount)
    dp.register_callback_query_handler(currency_expenses, state=MenuExpensesState.currency)
    dp.register_callback_query_handler(finish_expenses, state=MenuExpensesState.category)
    dp.register_callback_query_handler(money_box, Text(equals="money_box"))
    dp.register_callback_query_handler(current_goals_box, state=MoneyBoxState.current_goals)

