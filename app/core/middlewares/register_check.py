# from typing import Any, Awaitable, Callable, TypeVar
#
# from aiogram import Dispatcher, types
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import sessionmaker
#
# _T = TypeVar("_T", bound=types.TelegramObject)
# _RT = TypeVar("_RT")
# _DT = dict[str, Any]
#
#
# async def create_session(
#         handler: Callable[[_T, _DT], Awaitable[_RT]],
#         event: _T,
#         data: _DT,
# ) -> _RT:
#     session_factory: sessionmaker = data["session_factory"]
#     session: AsyncSession
#     async with session_factory() as session:
#         data["db"] = session
#         r = await handler(event, data)
#         await session.commit()
#     return r
#
#
# def setup(dp: Dispatcher) -> None:
#     dp.update.middleware(create_session)
