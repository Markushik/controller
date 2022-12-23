"""
The main file responsible for launching the bot
"""

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from loguru import logger
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine

from backend.core.database import get_session_maker
from backend.core.routers import setup_routers
from utils.commands import set_commands
from utils.config import settings


async def _main() -> None:
    """
    The main function responsible for launching the bot
    :return:
    """
    logger.add("../debug.log", format="{time} {level} {message}", level="DEBUG")
    logger.info("LAUNCHING BOT")

    storage_url = RedisStorage.from_url(url=f"redis://{settings.REDIS_HOST}")
    database_url = URL.create(
        drivername="postgresql+asyncpg",
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        username=settings.POSTGRES_USERNAME,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DATABASE,
    )

    bot = Bot(token=settings.API_TOKEN, parse_mode="HTML")
    disp = Dispatcher(storage=storage_url)

    router = setup_routers()
    disp.include_router(router)

    async_engine = create_async_engine(database_url)
    session_maker = get_session_maker(async_engine)

    try:
        await set_commands(bot)
        # await proceed_schemas(async_engine, BaseModel.metadata)
        await disp.start_polling(
            bot,
            session_maker=session_maker,
            allowed_updates=disp.resolve_used_update_types(),
        )
    finally:
        await disp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(_main())
    except (SystemExit, KeyboardInterrupt, ConnectionRefusedError):
        logger.warning("SHUTDOWN BOT")
