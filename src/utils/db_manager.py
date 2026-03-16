from src.database import async_session_maker, async_session_maker_null_pool


class DBManager:
    def __init__(self, session_factory=None):
        self.session_factory = session_factory or async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        from src.repositories.seller import SellerRepository
        self.seller = SellerRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
