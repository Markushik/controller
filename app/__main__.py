"""
The main file responsible for launching the bot
"""

import asyncio

from aiogram import Bot, Dispatcher
# from aiogram.fsm.storage.redis import RedisStorage
# test
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
# from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings
from app.core.routers import setup_routers
from app.utils.commands import set_commands


async def _main() -> None:
    """
    The main function responsible for launching the bot
    :return:
    """
    logger.info("START BOT")

    # engine = create_async_engine(
    #     f"postgresql+asyncpg://postgres:postgres@localhost/",
    #     future=True,
    #     echo=True,
    #
    # )

    storage = MemoryStorage()
    # storage = RedisStorage.from_url(url=f"redis://{settings.REDIS_HOST}")
    bot = Bot(settings.API_TOKEN, parse_mode="HTML")
    disp = Dispatcher(storage=storage)

    router = setup_routers()
    disp.include_router(router)

    await set_commands(bot)

    try:
        await disp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(_main())
    except (SystemExit, KeyboardInterrupt, ConnectionRefusedError):
        logger.warning("BOT OFF")
