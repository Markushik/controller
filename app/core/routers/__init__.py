"""
The file responsible for initializing routers
"""

from aiogram import Router
from aiogram.filters import Command

from . import client
from .routers import start
from ..middlewares.register_check import RegisterCheck


def setup_routers() -> Router:
    """
    Setup routers
    :return:
    """

    router = Router()
    router.include_router(client.router)

    router.message.register(start, Command(commands=["start"]))

    router.message.register(RegisterCheck)
    router.callback_query.register(RegisterCheck)

    return router
