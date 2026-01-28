from aiogram import Router
from src.keyboards.create_prediction import create_prediction_keyboard
from src.repositories.redis_repository import RedisRepository
from src.services.prediction_service import PredictionService
from src.services.auth_service import AuthService
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from src.states.auth import AuthStates


router = Router()

redis_repository = RedisRepository()
auth_service = AuthService(redis_repository=redis_repository)
prediction_service = PredictionService(redis_repository=redis_repository)

@router.message(Command("admin"))
async def admin_command_handler(message: Message, state: FSMContext) -> None:
    if message.chat.type == 'private':
        if await auth_service.is_admin_authenticated(message.from_user.id):
            await send_kb_to_admin(message)
            return
        else:
            await message.answer("Приветствую! Введите пожалуйста пароль👇")
            await state.set_state(AuthStates.password)

@router.message(AuthStates.password)
async def admin_password_handler(message: Message, state: FSMContext) -> None:
    password = message.text.strip()
    user_id = message.from_user.id

    if await auth_service.authenticate_admin(user_id, password):
        await message.answer("Аутентификация успешна!")
        await state.clear()
        await message.answer("Выберите действие:",  reply_markup=await create_prediction_keyboard())
    else:
        await message.answer("Неверный пароль. Попробуйте снова.")
        return

    
async def send_kb_to_admin(message: Message) -> None:
    await message.answer("Выберите действие:", reply_markup=await create_prediction_keyboard())
