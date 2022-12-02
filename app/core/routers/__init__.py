"""
The file responsible for initializing routers
"""

from aiogram import Router, F
from aiogram.filters import Command

from .routers import start, add_title_subscription, add_months_subscription
from ..states.storage import Form


def setup_routers() -> Router:
    """
    Setup routers
    :return:
    """

    router = Router()
    router.include_router(routers.router)

    router.message.register(start, Command(commands=["start"]))

    router.callback_query.register(add_title_subscription, F.data == "add_data")

    return router
