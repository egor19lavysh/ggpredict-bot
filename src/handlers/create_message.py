from aiogram import Router, F
from aiogram.types import ReplyKeyboardRemove
from src.keyboards.create_message import *
from src.keyboards.common import get_back_kb
from src.repositories.redis_repository import RedisRepository
from src.services.message_service import MessageService
from src.services.auth_service import AuthService
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.states.create_prediction import CreatePredictionStates
from .auth import send_kb_to_admin
from typing import Union


router = Router()

redis_repository = RedisRepository()
auth_service = AuthService(redis_repository=redis_repository)
message_service = MessageService(redis_repository=redis_repository)

@router.message(F.data == "messages")
async def show_messages(message: Message):
    await message.answer("Выберите действие:", reply_markup=await create_message_keyboard())

@router.callback_query(F.data == "create_message")
async def start_message(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Давайте создадим новое сообщение! Введите пожалуйста текст сообщения:", 
                                  reply_markup=get_back_kb())
    await state.set_state(CreatePredictionStates.text)

@router.message(CreatePredictionStates.text)
async def receive_message_text(message: Message, state: FSMContext) -> None:
    message_text = message.text.strip()

    if message_text.lower() == "назад":
        await message.answer("Создание сообщения отменено.", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        await send_kb_to_admin(message)
        return
    

    await message_service.create_message(
        text=message_text
    )

    await message.answer("Новое сообщение успешно создано!", reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await send_kb_to_admin(message)

