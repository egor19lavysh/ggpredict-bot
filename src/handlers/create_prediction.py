from aiogram import Router, F
from src.keyboards.create_prediction import *
from src.keyboards.common import get_back_kb
from src.repositories.redis_repository import RedisRepository
from src.services.prediction_service import PredictionService
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
prediction_service = PredictionService(redis_repository=redis_repository)


@router.callback_query(F.data == "create_prediction")
async def start_prediction(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Давайте создадим новое предсказание! Введите пожалуйста текст предсказания:", 
                                  reply_markup=get_back_kb())
    await state.set_state(CreatePredictionStates.text)

@router.message(CreatePredictionStates.text)
async def receive_prediction_text(message: Message, state: FSMContext) -> None:
    prediction_text = message.text.strip()

    if prediction_text.lower() == "назад":
        await message.answer("Создание предсказания отменено.", reply_markup=None)
        await state.clear()
        await send_kb_to_admin(message)
        return
    
    await state.update_data(text=prediction_text)
    
    await message.answer("Добавьте изображение к предсказанию. Поддерживаемые" \
                        "форматы: .jpg .jpeg .png .gif", reply_markup=await skip_kb(with_back=True))
    await state.set_state(CreatePredictionStates.image)

@router.callback_query(CreatePredictionStates.image)
@router.message(CreatePredictionStates.image)
async def receive_prediction_image(event: Union[Message, CallbackQuery], state: FSMContext) -> None:
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
        await message.delete()

        if event.data == "skip_image":
            await state.update_data(image=None)
        elif event.data == "skip_back":
            await message.answer("Давайте создадим новое предсказание! Введите пожалуйста текст предсказания:", 
                                  reply_markup=get_back_kb())
            await state.set_state(CreatePredictionStates.text)
            return
    else:
        message = event
        if message.photo:
            image_id = message.photo[-1].file_id
            await state.update_data(image=image_id)
        elif message.animation:
            await state.update_data(image=message.animation.file_id)
        else:
            await state.update_data(image=None)

    await message.answer("Это предсказание с призом? Если да, то какой приз выиграет участник:", 
                         reply_markup=await status_kb(with_back=True))
    await state.set_state(CreatePredictionStates.status)

@router.callback_query(CreatePredictionStates.status)
async def receive_prediction_status(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.edit_text("Выбран статус: " + callback.data.split("_")[1])


    if callback.data == "status_back":
        await callback.message.answer("Добавьте изображение к предсказанию. Поддерживаемые" \
                        "форматы: .jpg .jpeg .png .gif", reply_markup=await skip_kb(with_back=True))
        await state.set_state(CreatePredictionStates.image)
        return
    
    status_data = callback.data
    status = status_data.split("_")[1]
    await state.update_data(status=status)

    await callback.message.answer("Введите шанс выпадения предсказания числом.", 
                                  reply_markup=get_back_kb())
    await state.set_state(CreatePredictionStates.chance)

@router.message(CreatePredictionStates.chance)
async def receive_prediction_chance(message: Message, state: FSMContext) -> None:
    chance_text = message.text.strip()
    
    if chance_text.lower() == "назад":
        await message.answer("Это предсказание с призом? Если да, то какой приз выиграет участник:", 
                         reply_markup=await status_kb(with_back=True))
        await state.set_state(CreatePredictionStates.status)
        return
    
    try:
        chance_value = float(chance_text)
        if not (0 <= chance_value <= 100):
            raise ValueError
    except ValueError:
        await message.answer("Шанс должен быть числом от 0 до 100. Попробуйте снова.")
        return

    data = await state.get_data()
    text = data.get("text")
    image = data.get("image")
    status = data.get("status")

    await prediction_service.create_prediction(
        text=text,
        chance=chance_value,
        image=image,
        status=status
    )

    await message.answer("Новое предсказание успешно создано!")
    await state.clear()
    await send_kb_to_admin(message)

