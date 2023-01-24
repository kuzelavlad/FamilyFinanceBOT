from aiogram.dispatcher.filters.state import State, StatesGroup

class RegistationState(StatesGroup):
    username = State()
    password = State()
    # mail = State()

class LoginState(StatesGroup):
    username = State()
    password = State()

class MenuEarningState(StatesGroup):
    amount = State()
    currency = State()
    category = State()

class MenuExpensesState(StatesGroup):
    amount = State()
    currency = State()
    category = State()

class MoneyBoxState(StatesGroup):
    current_goals = State()
    add_new_goal = State()
