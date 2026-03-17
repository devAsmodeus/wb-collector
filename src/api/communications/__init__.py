"""Router: Коммуникации (09) — Вопросы, отзывы, чат (25 endpoints)."""
from litestar import Router

from src.api.communications.new_items import NewItemsController
from src.api.communications.questions import QuestionsController
from src.api.communications.feedbacks import FeedbacksController
from src.api.communications.pins import PinsController
from src.api.communications.chat import ChatController
from src.api.communications.claims import ClaimsController

communications_router = Router(
    path="/communications",
    route_handlers=[
        NewItemsController,
        QuestionsController,
        FeedbacksController,
        PinsController,
        ChatController,
        ClaimsController,
    ],
)
