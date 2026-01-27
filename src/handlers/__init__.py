from .auth import router as auth_router
from .create_prediction import router as create_prediction_router
from .list_predictions import router as list_predictions_router

routers = [
    auth_router,
    create_prediction_router,
    list_predictions_router,
]