"""
This file is responsible for displaying commands in the menu window
"""

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(
            command="start",
            description="Начать",
        )
    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault()
    )
