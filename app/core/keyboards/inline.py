from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu():
    buttons = [
        [
            InlineKeyboardButton(
                text="Действия с подписками",
                callback_data="actions_data"
            ),
        ],
        [
            InlineKeyboardButton(
                text="👤 Аккаунт",
                callback_data="account_data"
            ),
            InlineKeyboardButton(
                text="🆘 Поддержка",
                url="https://t.me/m_arqez/"
            ),
        ],
        [
            InlineKeyboardButton(
                text="💰 Донаты",
                callback_data="donate_data"
            ),
            InlineKeyboardButton(
                text="📊 Статистика",
                callback_data="statistics_data"
            ),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_subscription_actions():
    buttons = [
        [
            InlineKeyboardButton(
                text="Добавить",
                callback_data="add_data"
            ),
            InlineKeyboardButton(
                text="Изменить",
                callback_data="change_data"
            ),
            InlineKeyboardButton(
                text="Удалить",
                callback_data="delete_data"
            ),
        ],
        [
            InlineKeyboardButton(
                text="↩️ Вернуться",
                callback_data="back_data"
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_donate_menu():
    buttons = [
        [
            InlineKeyboardButton(
                text="☕ 199 ₽",
                url="https://www.donationalerts.com/r/marqrezz"
            ),
            InlineKeyboardButton(
                text="🍔 299 ₽",
                url="https://www.donationalerts.com/r/marqrezz"
            ),
            InlineKeyboardButton(
                text="🍕 499 ₽",
                url="https://www.donationalerts.com/r/marqrezz"
            ),
        ],
        [
            InlineKeyboardButton(
                text="↩️ Вернуться",
                callback_data="back_data"
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_main_back_menu():
    buttons = [
        [
            InlineKeyboardButton(
                text="Поделиться",
                switch_inline_query=''
            )
        ],
        [
            InlineKeyboardButton(
                text="↩️ Вернуться",
                callback_data="back_data"
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_first_back_reserve_menu():
    buttons = [
        [
            InlineKeyboardButton(
                text="↩️ Вернуться",
                callback_data="first_back_data"
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_confirm_or_reject_keyboard():
    buttons = [
        [
            InlineKeyboardButton(
                text="✅",
                callback_data="confirm_data"
            ),
            InlineKeyboardButton(
                text="❎",
                callback_data="reject_data"
            ),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
