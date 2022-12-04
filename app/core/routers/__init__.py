"""
The file responsible for initializing routers
"""

from aiogram import Router, F
from aiogram.filters import Command

from .routers import start, add_title_subscription, add_months_subscription, add_deadline_subscription, viewing_results, \
    confirm_result
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

    router.message.register(add_deadline_subscription, Form.months)
    router.message.register(viewing_results, Form.deadline)

    router.callback_query.register(confirm_result, F.data == "confirm_data")

    return router
