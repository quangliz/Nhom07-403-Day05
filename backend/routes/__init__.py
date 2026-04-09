from fastapi import APIRouter
from .chat import router as chat_router
from .analytics import router as analytics_router
from .feedback import router as feedback_router
from .menu import router as menu_router
from .eval import router as eval_router

router = APIRouter()
router.include_router(chat_router)
router.include_router(analytics_router)
router.include_router(feedback_router)
router.include_router(menu_router)
router.include_router(eval_router)
