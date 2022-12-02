from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    title = State()
    months = State()
    deadline = State()
    form = State()
