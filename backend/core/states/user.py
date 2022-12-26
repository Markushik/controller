"""
This file is responsible for using FSM
"""

from aiogram.fsm.state import State, StatesGroup


class UserForm(StatesGroup):
    service = State()
    months = State()
    deadline = State()
    reminder = State()
    form = State()
