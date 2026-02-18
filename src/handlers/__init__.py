from .auth import router as auth_router
from .create_message import router as create_message_router
from .list_messages import router as list_messages_router
from .delete_message import router as delete_message_router
from .edit_message import router as edit_message_router
from .list_bosses import router as list_bosses_router
from .hit import router as hit_router
from .control_boss import router as control_boss_router

routers = [
    auth_router,
    create_message_router,
    list_messages_router,
    delete_message_router,
    edit_message_router,
    list_bosses_router,
    hit_router,
    control_boss_router
]