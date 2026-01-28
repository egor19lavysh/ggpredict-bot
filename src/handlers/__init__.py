from .auth import router as auth_router
from .create_prediction import router as create_prediction_router
from .list_predictions import router as list_predictions_router
from .delete_prediction import router as delete_prediction_router
from .edit_prediction import router as edit_prediction_router
from .predict import router as predict_router

routers = [
    auth_router,
    create_prediction_router,
    list_predictions_router,
    delete_prediction_router,
    edit_prediction_router,
    predict_router
]