"""WB API proxy: Communications (09) — Вопросы, отзывы, чат."""
from litestar import Router

from src.api.communications.wb.new_items import NewItemsController
from src.api.communications.wb.questions import QuestionsController
from src.api.communications.wb.feedbacks import FeedbacksController
from src.api.communications.wb.pins import PinsController
from src.api.communications.wb.chat import ChatController
from src.api.communications.wb.claims import ClaimsController

communications_wb_router = Router(
    path="/wb",
    route_handlers=[
        NewItemsController,
        QuestionsController,
        FeedbacksController,
        PinsController,
        ChatController,
        ClaimsController,
    ],
)
