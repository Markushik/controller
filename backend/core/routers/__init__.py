"""
The file responsible for initializing routers
"""

from aiogram import Router

from .routers import (add_deadline_subscription, add_months_subscription,
                      add_title_subscription, confirm_result, start,
                      viewing_results)

__all__ = [
    "setup_routers",
    "start",
    "add_title_subscription",
    "add_deadline_subscription",
    "add_months_subscription",
    "viewing_results",
    "confirm_result",
]


def setup_routers() -> Router:
    """
    Setup routers
    :return:
    """

    router = Router()
    router.include_router(routers.router)

    return router