"""Litestar dependencies — provide() функции для DI."""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.utils.db_manager import DBManager


async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Предоставляет сессию SQLAlchemy для контроллеров."""
    async with async_session_maker() as session:
        yield session


async def provide_db_manager() -> AsyncGenerator[DBManager, None]:
    """Предоставляет DBManager (репозитории) для контроллеров."""
    async with DBManager() as db:
        yield db
