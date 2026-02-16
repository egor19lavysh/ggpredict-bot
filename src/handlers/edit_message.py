from aiogram import Router, F
from src.handlers.list_messages import edit_message
from src.keyboards.create_message import *
from src.repositories.redis_repository import RedisRepository
from src.services.message_service import MessageService
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from src.states.edit_prediction import EditPredictionStates
from .auth import send_kb_to_admin
from typing import Union



router = Router()

redis_repository = RedisRepository()
message_service = MessageService(redis_repository=redis_repository)


@router.callback_query(F.data == "edit_text")
async def start_edit_text(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Введите новый текст сообщения:")
    await state.set_state(EditPredictionStates.text)


@router.message(EditPredictionStates.text)
async def receive_edit_text(message: Message, state: FSMContext) -> None:
    prediction_text = message.text.strip()
    
    data = await state.get_data()
    message_id = data.get("message_id")
    
    await message_service.update_message_text(message_id, prediction_text)
    await message.answer("Текст сообщения успешно обновлен!")
    
    await state.clear()
    await send_kb_to_admin(message)


@router.callback_query(F.data == "edit_back")
async def edit_back(callback: CallbackQuery, state: FSMContext) -> None:
    await edit_message(callback, state)

