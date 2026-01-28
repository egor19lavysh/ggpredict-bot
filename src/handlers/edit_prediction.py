from aiogram import Router, F
from src.keyboards.create_prediction import skip_kb, status_kb, edit_prediction_fields_kb
from src.repositories.redis_repository import RedisRepository
from src.services.prediction_service import PredictionService
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from src.states.edit_prediction import EditPredictionStates
from .auth import send_kb_to_admin
from typing import Union
from .list_predictions import edit_prediction


router = Router()

redis_repository = RedisRepository()
prediction_service = PredictionService(redis_repository=redis_repository)


@router.callback_query(F.data == "edit_text")
async def start_edit_text(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Введите новый текст предсказания:")
    await state.set_state(EditPredictionStates.text)


@router.message(EditPredictionStates.text)
async def receive_edit_text(message: Message, state: FSMContext) -> None:
    prediction_text = message.text.strip()
    
    data = await state.get_data()
    prediction_id = data.get("prediction_id")
    
    await prediction_service.update_prediction_text(prediction_id, prediction_text)
    await message.answer("Текст предсказания успешно обновлен!")
    
    await state.clear()
    await send_kb_to_admin(message)


@router.callback_query(F.data == "edit_image")
async def start_edit_image(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Добавьте новое изображение к предсказанию. Поддерживаемые форматы: .jpg .jpeg .png .gif", 
                                  reply_markup=await skip_kb())
    await state.set_state(EditPredictionStates.image)


@router.callback_query(EditPredictionStates.image)
@router.message(EditPredictionStates.image)
async def receive_edit_image(event: Union[Message, CallbackQuery], state: FSMContext) -> None:
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
        await message.delete()
        image_id = None
    else:
        message = event
        if message.photo:
            image_id = message.photo[-1].file_id
        elif message.animation:
            image_id = message.animation.file_id
        else:
            image_id = None

    data = await state.get_data()
    prediction_id = data.get("prediction_id")
    
    await prediction_service.update_prediction_image(prediction_id, image_id)
    await message.answer("Изображение предсказания успешно обновлено!")
    
    await state.clear()
    await send_kb_to_admin(message)


@router.callback_query(F.data == "edit_status")
async def start_edit_status(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Это предсказание с призом? Если да, то какой приз выиграет участник:", 
                                  reply_markup=await status_kb())
    await state.set_state(EditPredictionStates.status)


@router.callback_query(EditPredictionStates.status)
async def receive_edit_status(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.edit_text("Выбран статус: " + callback.data.split("_")[1])
    status = callback.data.split("_")[1]
    
    data = await state.get_data()
    prediction_id = data.get("prediction_id")
    
    await prediction_service.update_prediction_status(prediction_id, status)
    await callback.message.answer("Статус предсказания успешно обновлен!")
    
    await state.clear()
    await send_kb_to_admin(callback.message)


@router.callback_query(F.data == "edit_chance")
async def start_edit_chance(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Введите новый шанс выпадения предсказания числом и процентом без пробела между ними. Например: 50%")
    await state.set_state(EditPredictionStates.chance)


@router.message(EditPredictionStates.chance)
async def receive_edit_chance(message: Message, state: FSMContext) -> None:
    chance_text = message.text.strip()
    if not chance_text.endswith("%"):
        await message.answer("Пожалуйста, введите шанс в правильном формате, например: 50%")
        return

    try:
        chance_value = float(chance_text[:-1])
        if not (0 <= chance_value <= 100):
            raise ValueError
    except ValueError:
        await message.answer("Шанс должен быть числом от 0 до 100. Попробуйте снова.")
        return

    data = await state.get_data()
    prediction_id = data.get("prediction_id")
    
    await prediction_service.update_prediction_chance(prediction_id, chance_value)
    await message.answer("Шанс предсказания успешно обновлен!")
    
    await state.clear()
    await send_kb_to_admin(message)


@router.callback_query(F.data == "edit_back")
async def edit_back(callback: CallbackQuery, state: FSMContext) -> None:
    await edit_prediction(callback, state)

