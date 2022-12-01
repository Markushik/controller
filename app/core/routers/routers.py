"""
The file responsible for use commands in bot
"""
import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands="start"))
async def send_pong(message: Message) -> None:
    pong = ""
    hostname = '127.0.0.1'
    response = os.system('ping -c 5 ' + hostname)
    if response == 0:
        pong = (' is up!')
    else:
        pong = (' is down!')
    await message.reply(pong)
