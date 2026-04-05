"""DB: Communications (09)."""
from litestar import Router
from src.api.communications.db.feedbacks import DbFeedbacksController
from src.api.communications.db.questions import DbQuestionsController
from src.api.communications.db.claims import DbClaimsController
from src.api.communications.db.chats import DbChatsController

communications_db_router = Router(
    path="/db",
    route_handlers=[
        DbFeedbacksController, DbQuestionsController, DbClaimsController, DbChatsController,
    ],
)
