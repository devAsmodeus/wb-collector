from src.database import async_session_maker, async_session_maker_null_pool


class DBManager:
    def __init__(self, session_factory=None):
        self.session_factory = session_factory or async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        from src.repositories.general.seller import SellerRepository
        from src.repositories.general.rating import RatingRepository
        from src.repositories.general.subscriptions import SubscriptionsRepository
        self.seller = SellerRepository(self.session)
        self.rating = RatingRepository(self.session)
        self.subscriptions = SubscriptionsRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
