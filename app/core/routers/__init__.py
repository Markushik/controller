"""
The file responsible for initializing routers
"""

from aiogram import Router

from . import client


def setup_routers() -> Router:
    router = Router()
    router.include_router(client.router)

    return router
