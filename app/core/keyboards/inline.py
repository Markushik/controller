from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_subscription_actions():
    buttons = [
        [
            InlineKeyboardButton(text="Добавить", callback_data="add_data"),
            InlineKeyboardButton(text="Изменить", callback_data="change_data"),
            InlineKeyboardButton(text="Удалить", callback_data="delete_data"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_confirm_or_reject_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="✅", callback_data="confirm_data"),
            InlineKeyboardButton(text="❎", callback_data="reject_data"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
