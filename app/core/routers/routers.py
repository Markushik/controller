"""
The file responsible for use commands in bot
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.core.keyboards.inline import get_confirm_or_reject_keyboard, get_subscription_actions
from app.core.states.storage import Form

router = Router()


async def start(message: Message) -> None:
    await message.answer(
        text="<b>CONTROLLER</b> — время напомнить об истечении твоей подписки\n\n"
             "<b>Что вы хотите сделать?</b>",
        reply_markup=get_subscription_actions(),
    )


async def add_title_subscription(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.title)

    await query.message.edit_text(
        text="<b>Как называется ваша подписка?</b>"
    )


@router.message(Form.title)
async def add_months_subscription(message: Message, state: FSMContext) -> None:
    await message.delete()
