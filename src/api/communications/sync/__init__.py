"""Sync: Communications (09)."""
from litestar import Router
from src.api.communications.sync.feedbacks import SyncFeedbacksController
from src.api.communications.sync.questions import SyncQuestionsController
from src.api.communications.sync.claims import SyncClaimsController

communications_sync_router = Router(
    path="/sync",
    route_handlers=[
        SyncFeedbacksController, SyncQuestionsController, SyncClaimsController,
    ],
)
