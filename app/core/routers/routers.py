"""
The file responsible for use commands in bot
"""
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message
from aiogram.utils.deep_linking import create_start_link
from aioredis import Redis
from sqlalchemy.orm import sessionmaker

from app.core.database import User
from app.core.keyboards.inline import (get_confirm_or_reject_keyboard,
                                       get_donate_menu,
                                       get_first_back_reserve_menu,
                                       get_main_back_menu, get_main_menu,
                                       get_subscription_actions)
from app.core.states.storage import Form

router = Router()
redis = Redis()


def get_datetime() -> str:
    return str(datetime.now())


@router.message(Command(commands=["start"]))
async def start(message: Message, session_maker: sessionmaker) -> None:
    await redis.set(str(message.from_user.id), get_datetime(), nx=True)
    await redis.sadd("users_count", str(message.from_user.id))

    async with session_maker() as session:
        async with session.begin():
            session.add(
                User(
                    user_id=int(message.from_user.id),
                    user_name=str(message.from_user.first_name)

                )
            )
            await session.commit()

    await message.answer_photo(
        photo=FSInputFile(
            "C:/Users/Zemik/Documents/GitHub/controller/app/assets/images/menu.png"
        ),
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "actions_data")
async def start_reserve(query: CallbackQuery) -> None:
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(
                'C:/Users/Zemik/Documents/GitHub/controller/app/assets/images/menu.png'
            ),
            caption="<b>🗂️ Каталог активных подписок:</b>\n\n"
                    "У вас не имеется <b>активных</b> подписок 🤷‍♂️"
        ),
        reply_markup=get_subscription_actions(),
    )
    await query.answer()


@router.callback_query(F.data == "add_data")  # Добавить
async def add_title_subscription(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(
                'C:/Users/Zemik/Documents/GitHub/controller/app/assets/images/menu.png'
            ),
            caption="— Как называется <b>сервис</b> на который вы <b>подписались</b>?\n\n"
                    "<b>Пример:</b> <code>Tinkoff Premium</code>"
        )
    )

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
    except ValueError:
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
             f"<b>Оповестить за</b> <code>{user_data['reminder']} (д.)</code>",
        reply_markup=get_confirm_or_reject_keyboard()
    )


@router.callback_query(F.data == "confirm_data")
async def confirm_result(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_text(
        text="<b>✅ Успех:</b> Данные были успешно записаны",
        reply_markup=get_first_back_reserve_menu()
    )
    await state.clear()
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


@router.callback_query(F.data == "first_back_data")
async def start_second_reserve(query: CallbackQuery) -> None:
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(
                'C:/Users/Zemik/Documents/GitHub/controller/app/assets/images/menu.png'
            ),
            caption="<b>🗂️ Каталог активных подписок:</b>\n\n"
                    "У вас не имеется <b>активных</b> подписок 🤷‍♂️"
        ),
        reply_markup=get_subscription_actions(),
    )
    await query.answer()


@router.callback_query(F.data == "back_data")
async def start_first_reserve(query: CallbackQuery) -> None:
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(
                'C:/Users/Zemik/Documents/GitHub/controller/app/assets/images/menu.png'
            )
        ),
        reply_markup=get_main_menu()
    )
    await query.answer()


@router.callback_query(F.data == "account_data")
async def account_data(query: CallbackQuery, bot: Bot) -> None:
    date = await redis.get(str(query.from_user.id))
    link = await create_start_link(bot=bot, payload=str(query.from_user.id), encode=True)

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(
                'C:/Users/Zemik/Documents/GitHub/controller/app/assets/images/menu.png'
            ),
            caption=f"<b>🆔 Ваш ID:</b> <code>{query.from_user.id}</code>\n"
                    f"<b>📅 Регистрация:</b> <code>{str(date, 'utf-8')[:-7]}</code>\n"
                    f"<b>👥 Приглашено:</b> <code>5 (чел.)</code>\n\n"
            # #202 Редиска считает кол-во переходов по ссылке и выводит значение
                    f"<b>🔗 Ваша реферальная ссылка:</b>\n"
                    f"<code>{link}</code>"
        ),
        reply_markup=get_main_back_menu(),
    )
    await query.answer()


@router.callback_query(F.data == "donate_data")
async def author_support(query: CallbackQuery) -> None:
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(
                'C:/Users/Zemik/Documents/GitHub/controller/app/assets/images/menu.png'
            )
        ),
        reply_markup=get_donate_menu()
    )
    await query.answer()


@router.callback_query(F.data == "statistics_data")
async def users_statistics(query: CallbackQuery) -> None:
    # users = await redis.scard("users_count")
    pass
    await query.answer()
