"""
The file responsible for use commands in bot
"""

from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, ContentType, FSInputFile,
                           InputMediaPhoto, Message)
from aiogram.utils.deep_linking import create_start_link
from aioredis import Redis
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, ProgrammingError
from sqlalchemy.orm import sessionmaker

from src.app.core.database.tables import Service, User
from src.app.core.keyboards.inline import (get_confirm_or_reject_keyboard,
                                       get_donate_menu,
                                       get_first_back_reserve_menu,
                                       get_main_back_menu, get_main_menu,
                                       get_subscription_actions)
from src.app.core.states.user import UserForm

router = Router()
redis = Redis()


def get_datetime() -> str:
    return str(datetime.now())


async def get_user(user_id: int, session_maker: sessionmaker) -> User:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User)
                .filter(User.user_id == user_id)
            )
            return result.scalars().one()


async def create_user(user_id: int, username: str, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            session.add(
                User(
                    user_id=user_id,
                    username=username

                )
            )
            await session.commit()


@router.message(Command(commands=["start"]))
async def start(message: Message, session_maker: sessionmaker) -> None:
    await redis.set(str(message.from_user.id), get_datetime(), nx=True)
    await redis.sadd("users_count", str(message.from_user.id))

    try:
        await get_user(message.from_user.id, session_maker)
    except (ProgrammingError, NoResultFound):
        await create_user(message.from_user.id, message.from_user.first_name, session_maker)

    await message.answer_photo(
        photo=FSInputFile(
            "C:/Users/Zemik/PycharmProjects/controller/assets/images/main-menu.png"
        ),
        reply_markup=get_main_menu(),
    )


@router.callback_query(F.data == "actions_data")
async def start_reserve(query: CallbackQuery) -> None:
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(
                "C:/Users/Zemik/PycharmProjects/controller/assets/images/main-menu.png"
            ),
            caption="<b>🗂️ Каталог активных подписок:</b>\n\n"
                    "У вас не имеется <b>активных</b> подписок 🤷‍♂️",
        ),
        reply_markup=get_subscription_actions(),
    )
    await query.answer()


@router.callback_query(F.data == "add_data")  # Добавить
async def add_title_subscription(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(
                "C:/Users/Zemik/PycharmProjects/controller/assets/images/main-menu.png"
            ),
            caption="— Как называется <b>сервис</b> на который вы <b>подписались</b>?\n\n"
                    "<b>Пример:</b> <code>Tinkoff Premium</code>",
        )
    )

    await state.set_state(UserForm.service)
    await query.answer()


@router.message(UserForm.service)
async def add_months_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await message.answer(
        text="— Сколько <b>месяцев</b> будет действовать подписка?\n\n"
             "<b>Пример:</b> <code>12 (мес.)</code>",
    )
    await state.set_state(UserForm.months)


@router.message(UserForm.months)
async def add_deadline_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(months=message.text)

    if message.text.isdigit() and int(message.text) != 0 and int(message.text) <= 12:
        pass
    else:
        await message.answer(text="<b>🚫 Ошибка:</b> Недопустимые символы")
        return

    await state.set_state(UserForm.reminder)
    await message.answer(
        text="— В какую <b>дату</b> произойдет списание средств?\n\n"
             "<b>Пример:</b> <code>12-12-2023</code>"
    )


@router.message(UserForm.reminder)
async def add_reminder_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(deadline=message.text)

    try:
        datetime.strptime(message.text, "%d-%m-%Y")
        pass
    except ValueError:
        await message.answer(text="<b>🚫 Ошибка:</b> Неверный формат")
        return

    await state.set_state(UserForm.deadline)
    await message.answer(
        text="— За сколько <b>дней</b> оповещать о ближайшем списании?\n\n"
             "<b>Пример:</b> <code>2 (д.)</code>"
    )


@router.message(UserForm.deadline)
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
        reply_markup=get_confirm_or_reject_keyboard(),
    )


@router.callback_query(F.data == "confirm_data")
async def confirm_result(
        query: CallbackQuery, state: FSMContext, session_maker: sessionmaker
) -> None:
    user_data = await state.get_data()

    await query.message.edit_text(
        text="<b>✅ Успех:</b> Данные были успешно записаны",
        reply_markup=get_first_back_reserve_menu(),
    )

    async with session_maker() as session:
        async with session.begin():
            session.add(
                Service(
                    service=str(user_data["title"]),
                    months=int(user_data["months"]),
                    deadline=str(user_data["deadline"]),
                    reminder=int(user_data["reminder"]),
                )
            )
            await session.commit()

    await state.clear()
    await query.answer()


@router.callback_query(F.data == "reject_data")
async def overwriting_data(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_text(
        text="— Как называется <b>сервис</b> на который вы <b>подписались</b>?\n\n"
             "<b>Пример:</b> <code>Tinkoff Pro</code>"
    )
    await state.clear()
    await state.set_state(UserForm.service)
    await query.answer()


@router.callback_query(F.data == "first_back_data")
async def start_second_reserve(query: CallbackQuery) -> None:
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(
                "C:/Users/Zemik/PycharmProjects/controller/assets/images/main-menu.png"
            ),
            caption="<b>🗂️ Каталог активных подписок:</b>\n\n"
                    "У вас не имеется <b>активных</b> подписок 🤷‍♂️",
        ),
        reply_markup=get_subscription_actions(),
    )
    await query.answer()


@router.callback_query(F.data == "back_data")
async def start_first_reserve(query: CallbackQuery) -> None:
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(
                "C:/Users/Zemik/PycharmProjects/controller/assets/images/main-menu.png"
            )
        ),
        reply_markup=get_main_menu(),
    )
    await query.answer()


@router.callback_query(F.data == "account_data")
async def account_data(query: CallbackQuery, bot: Bot) -> None:
    date = await redis.get(str(query.from_user.id))
    link = await create_start_link(
        bot=bot, payload=str(query.from_user.id), encode=True
    )

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(
                "C:/Users/Zemik/PycharmProjects/controller/assets/images/main-menu.png"
            ),
            caption=f"<b>🆔 Ваш ID:</b> <code>{query.from_user.id}</code>\n"
                    f"<b>📅 Регистрация:</b> <code>{str(date, 'utf-8')[:-7]}</code>\n"
                    f"<b>👥 Приглашено:</b> <code>5 (чел.)</code>\n\n"
            # #202 Редиска считает кол-во переходов по ссылке и выводит значение
                    f"<b>🔗 Ваша реферальная ссылка:</b>\n" f"<code>{link}</code>",
        ),
        reply_markup=get_main_back_menu(),
    )
    await query.answer()


@router.callback_query(F.data == "donate_data")
async def author_support(query: CallbackQuery) -> None:
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(
                "C:/Users/Zemik/PycharmProjects/controller/assets/images/main-menu.png"
            )
        ),
        reply_markup=get_donate_menu(),
    )
    await query.answer()


@router.message(F.content_type_in(ContentType.WEB_APP_DATA))
async def users_statistics(query: CallbackQuery) -> None:
    # users = await redis.scard("users_count")
    pass
    await query.answer()
