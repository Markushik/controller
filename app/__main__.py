"""
The main file responsible for launching the bot
"""

import asyncio

from aiogram import Bot, Dispatcher
# from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
from sqlalchemy.engine import URL

from app.config import settings
from app.core.database import create_async_engine, get_session_maker, proceed_schemas
from app.core.database.base import BaseModel
from app.core.middlewares.register_check import RegisterCheck
from app.core.routers import setup_routers
from app.utils.commands import set_commands


# from sqlalchemy.ext.asyncio import create_async_engine


async def _main() -> None:
    """
    The main function responsible for launching the bot
    :return:
    """
    logger.info("START BOT")

    storage = MemoryStorage()
    # storage = RedisStorage.from_url(url=f"redis://{settings.REDIS_HOST}")
    bot = Bot(settings.API_TOKEN, parse_mode="HTML")
    disp = Dispatcher(storage=storage)

    postgres_url = URL.create(
        drivername="postgresql+asyncpg",
        username=settings.POSTGRES_USERNAME,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT
    )

    disp.message.middleware(RegisterCheck())
    disp.callback_query.middleware(RegisterCheck())

    router = setup_routers()
    disp.include_router(router)

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)

    try:
        await set_commands(bot)
        await bot.get_updates(offset=-1)
        await disp.start_polling(bot, session_maker=session_maker)
    finally:
        await disp.fsm.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(_main())
    except (SystemExit, KeyboardInterrupt, ConnectionRefusedError):
        logger.warning("BOT OFF")
