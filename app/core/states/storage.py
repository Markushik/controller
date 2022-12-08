from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    service = State()
    months = State()
    deadline = State()
    reminder = State()
    form = State()
