from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from src.services.prediction_service import PredictionService
from .auth import send_kb_to_admin


router = Router()
prediction_service = PredictionService()

@router.callback_query(F.data.startswith("confirm_"))
async def confirm_delete_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    choice = callback.data.split("_")[-1]
    data = await state.get_data()

    try:
        prediction_id = data["prediction_id"]
    except Exception as e:
        await callback.message.answer("Я потерял предсказание. Попробуйте еще раз.")

    if choice == "да":
        await prediction_service.delete_prediction(prediction_id=prediction_id)
        await callback.message.answer("Предсказание удалено. Я не плачу, это просто пиксели😭")
    else:
        await callback.message.answer("Удаление отменено.")

    await state.clear()

    await send_kb_to_admin(callback.message)

