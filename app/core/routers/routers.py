"""
The file responsible for use commands in bot
"""

from datetime import datetime

import aiofiles
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile, InputFile, URLInputFile

from app.core.keyboards.inline import \
    get_confirm_or_reject_keyboard, \
    get_subscription_actions, \
    get_main_menu, \
    get_donate_menu, \
    get_first_back_reserve_menu
from app.core.states.storage import Form

router = Router()


@router.message(Command(commands=["start"]))
async def start(message: Message) -> None:
    await message.answer_photo(
        photo="https://i.postimg.cc/xj8Njpnr/main.png?dl=1",
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "back_data")
async def start_first_reserve(query: CallbackQuery) -> None:
    await query.message.edit_text(
        text="<b>👨‍✈️ CONTROLLER</b> — время напомнить об истечении твоей подписки\n\n",
        reply_markup=get_main_menu(),
    )
    await query.answer()


@router.callback_query(F.data == "first_back_data")
async def start_second_reserve(query: CallbackQuery) -> None:
    await query.message.edit_text(
        text="<b>🗂️ Каталог активных подписок:</b>\n\n"
             "У вас не имеется <b>активных</b> подписок 🤷‍♂️",
        reply_markup=get_subscription_actions(),
    )
    await query.answer()


@router.callback_query(F.data == "actions_data")
async def start_reserve(query: CallbackQuery) -> None:
    await query.message.edit_text(
        text="<b>🗂️ Каталог активных подписок:</b>\n\n"
             "У вас не имеется <b>активных</b> подписок 🤷‍♂️",
        reply_markup=get_subscription_actions(),
    )
    await query.answer()


@router.callback_query(F.data == "add_data")
async def add_title_subscription(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_text(
        text="— Как называется <b>сервис</b> на который вы <b>подписались</b>?\n\n"
             "<b>Пример:</b> <code>Tinkoff Pro</code>"
    )
    await state.set_state(Form.service)
    await query.answer()


@router.callback_query(F.data == "reject_data")
async def overwriting_data(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_text(
        text="— Как называется <b>сервис</b> на который вы <b>подписались</b>?\n\n"
             "<b>Пример:</b> <code>Tinkoff Pro</code>"
    )
    await state.clear()
    await state.set_state(Form.service)
    await query.answer()


@router.message(Form.service)
async def add_months_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await message.answer(
        text="— Сколько <b>месяцев</b> будет действовать подписка?\n\n"
             "<b>Пример:</b> <code>12 (мес.)</code>",
    )
    await state.set_state(Form.months)


@router.message(Form.months)
async def add_deadline_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(months=message.text)

    if message.text.isdigit() and int(message.text) != 0 and int(message.text) <= 12:
        # TODO ⚠️ Не больше 12 месяцев
        pass
    else:
        await message.answer(text="<b>🚫 Ошибка:</b> Недопустимые символы")
        return

    await state.set_state(Form.reminder)
    await message.answer(
        text="— В какую <b>дату</b> произойдет списание средств?\n\n"
             "<b>Пример:</b> <code>12.12.2023</code>"
    )


@router.message(Form.reminder)
async def add_reminder_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(deadline=message.text)

    try:
        datetime.strptime(message.text, '%d.%m.%Y')
        pass
    except Exception:
        await message.answer(text="<b>🚫 Ошибка:</b> Неверный формат")
        return

    await state.set_state(Form.deadline)
    await message.answer(
        text="— За сколько <b>дней</b> оповещать о ближайшем списании?\n\n"
             "<b>Пример:</b> <code>2 (д.)</code>"
    )


@router.message(Form.deadline)
async def viewing_results(message: Message, state: FSMContext) -> None:
    await state.update_data(reminder=message.text)
    user_data = await state.get_data()

    if message.text.isdigit() and int(message.text) != 0 and int(message.text) <= 7:
        pass
    else:
        await message.answer(text="<b>🚫 Ошибка:</b> Недопустимые символы")
        return

    await message.answer(
        text="📩 Проверьте <b>правильность</b> введённых данных:\n\n"
             f"<b>Сервис:</b> <code>{user_data['title']}</code>\n"
             f"<b>Длительность:</b> <code>{user_data['months']} (мес.)</code>\n"
             f"<b>Окончание:</b> <code>{user_data['deadline']}</code>\n"
             f"<b>Оповестить за:</b> <code>{user_data['reminder']} (д.)</code>",
        reply_markup=get_confirm_or_reject_keyboard()
    )


@router.callback_query(F.data == "confirm_data")
async def confirm_result(query: CallbackQuery) -> None:
    await query.message.edit_text(
        text="<b>✅ Успех:</b> Данные были успешно записаны",
        reply_markup=get_first_back_reserve_menu()
    )
    await query.answer()


# @router.callback_query(F.data == "donate_data")
# async def author_support(query: CallbackQuery) -> None:
#     await query.message.edit_media(
#         media=URLInputFile(url="https://i.postimg.cc/xj8Njpnr/main.png?dl=1")
#     )
#     await query.answer()


@router.callback_query(F.data == "account_data")
async def account_data(query: CallbackQuery) -> None:
    await query.message.edit_text(
        text=f"<b>🆔 Ваш ID:</b> <code>{query.from_user.id}</code>\n"
             f"<b>🗓️ Регистрация:</b> <code>08.12.2022</code>\n"
             f"<b>Подписок:</b> <code>15</code>\n"
             f"<b>👥 Приглашено:</b> <code>5</code>\n\n"
             f"<b>🔗 Реферальная ссылка:</b>\n"
             f"<code>https://t.me/jopagamebot?start={query.from_user.id}</code>"
    )


@router.callback_query(F.data == "statistics_data")
async def users_statistics(query: CallbackQuery) -> None:
    await query.message.edit_text(
        text="test"  # web-app
    )
    await query.answer()
