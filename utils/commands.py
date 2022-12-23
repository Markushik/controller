"""
This file is responsible for displaying commands in the menu window
"""

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    """
    Create menu commands
    :param bot:
    :return:
    """
    commands = [
        BotCommand(
            command="start",
            description="start bot",
        ),
    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault(),
    )
