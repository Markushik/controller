"""
The file responsible for use commands in bot
"""

from aiogram import Router
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
        text="<b>Введите название вашей подписки</b>"
    )
    await query.answer()


@router.callback_query(Form.title)
async def add_months_subscription(query: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(title=query.message.text)
    await state.set_state(Form.months)
    await query.message.answer(
        text="<b>Введите количетсво месяцев</b>"
    )


async def add_deadline_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(months=message.text)
    await state.set_state(Form.deadline)
    await message.answer(
        text="<b>Введите окончание подписки</b>"
    )


async def viewing_results(message: Message, state: FSMContext) -> None:
    await state.update_data(deadline=message.text)
    user_data = await state.get_data()

    await message.answer(
        text="Проверьте правильность введенных данных:\n"
             f"Наименование: {user_data['title']}\n"
             f"Длительность: {user_data['months']}\n"
             f"Окончание: {user_data['deadline']}\n",
        reply_markup=get_confirm_or_reject_keyboard()
    )

async def confirm_result(message: Message, state: FSMContext) -> None:
    await message.answer("все норм")
