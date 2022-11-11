"""
The file responsible for use commands in bot
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands="start"))
async def cmd_settings(message: Message) -> None:
    """
    Handling the "/settings" command
    :param message:
    :return:
    """
    await message.answer("#TODO")
