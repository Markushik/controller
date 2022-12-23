from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    service = State()
    months = State()
    deadline = State()
    reminder = State()
    form = State()
