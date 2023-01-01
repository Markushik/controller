"""
This file is responsible for displaying inline-buttons.
"""

from aiogram.types import (InlineKeyboardButton, WebAppInfo)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.row(
        InlineKeyboardButton(text="Действия с подписками", callback_data="actions_data")
    )
    menu_builder.row(
        InlineKeyboardButton(text="👤 Аккаунт", callback_data="account_data"),
        InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/m_arqez/"),
    )
    menu_builder.row(
        InlineKeyboardButton(text="💰 Донаты", callback_data="donate_data"),
        InlineKeyboardButton(text="📊 Статистика", web_app=WebAppInfo(url="https://markushik.github.io/controller/")),
    )

    return menu_builder.as_markup()


def get_subscription_actions():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.row(
        InlineKeyboardButton(text="Добавить", callback_data="add_data"),
        InlineKeyboardButton(text="Изменить", callback_data="change_data"),
        InlineKeyboardButton(text="Удалить", callback_data="delete_data"),
    )
    menu_builder.row(
        InlineKeyboardButton(text="↩️ Вернуться", callback_data="back_data")
    )

    return menu_builder.as_markup()


def get_donate_menu():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.row(
        InlineKeyboardButton(text="☕ 199 ₽", url="https://github.com/Markushik/controller/"),  # pay=True
        InlineKeyboardButton(text="🍔 299 ₽", url="https://github.com/Markushik/controller/"),
        InlineKeyboardButton(text="🍕 499 ₽", url="https://github.com/Markushik/controller/")
    )
    menu_builder.row(
        InlineKeyboardButton(text="↩️ Вернуться", callback_data="back_data")
    )

    return menu_builder.as_markup()


def get_main_back_menu():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.row(
        InlineKeyboardButton(text="↩️ Вернуться", callback_data="back_data"),
        InlineKeyboardButton(text="📨 Поделиться", switch_inline_query=""),
    )

    return menu_builder.as_markup()


def get_first_back_reserve_menu():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.row(
        InlineKeyboardButton(text="↩️ Вернуться", callback_data="first_back_data"),
    )

    return menu_builder.as_markup()


def get_confirm_or_reject_keyboard():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.row(
        InlineKeyboardButton(text="✅", callback_data="confirm_data"),
        InlineKeyboardButton(text="❎", callback_data="reject_data"),
    )

    return menu_builder.as_markup()
