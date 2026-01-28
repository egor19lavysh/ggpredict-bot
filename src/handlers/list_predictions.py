from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from src.services.prediction_service import PredictionService
from src.keyboards.common import predictions_keyboard
from src.keyboards.create_prediction import delete_confirm_kb, edit_prediction_fields_kb
from aiogram.fsm.context import FSMContext
from src.models.prediction import Prediction
from aiogram.exceptions import TelegramBadRequest
from .auth import send_kb_to_admin


router = Router()
prediction_service = PredictionService()


@router.callback_query(F.data.in_(("edit_prediction", "delete_prediction")))
async def edit_prediction(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    predictions = await prediction_service.get_all_predictions()

    await state.update_data(action=callback.data.split("_")[0])
    await callback.message.answer("Выберите предсказание:", reply_markup=predictions_keyboard(predictions))

@router.callback_query(F.data.startswith("predictions_page_"))
async def show_predictions_page(callback: CallbackQuery):
    await callback.answer()

    page = int(callback.data.split("_")[-1])
    predictions = await prediction_service.get_all_predictions()
    keyboard = predictions_keyboard(predictions, current_page=page)
    
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    

async def show_prediction(bot: Bot, chat_id: int, prediction: Prediction):
    prediction_text = f"Предсказание: {prediction.text}\nСтатус: {prediction.status}\nШанс: {prediction.chance}%"
    if prediction.image:
        try:
            await bot.send_photo(
                    chat_id,
                    photo=prediction.image,
                    caption=prediction_text
                )
        except TelegramBadRequest:
            await bot.send_animation(
                    chat_id,
                    animation=prediction.image,
                    caption=f"Предсказание: {prediction.text}\nСтатус: {prediction.status}\nШанс: {prediction.chance}%"
                )
        except Exception as e:
            await bot.send_message(chat_id=chat_id, text="Произошла какая-то ошибка. Бот не смог отправить предсказание")
            print(e)
    else:
        await bot.send_message(
                    chat_id,
                    text=f"Предсказание: {prediction.text}\nСтатус: {prediction.status}\nШанс: {prediction.chance}%"
                )

@router.callback_query(F.data.startswith("prediction_"))
async def show_prediction_detail(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete*()
    
    prediction_id = int(callback.data.split("_")[-1])
    await state.update_data(prediction_id=prediction_id)
    prediction = await prediction_service.get_prediction_by_id(prediction_id)

    data = await state.get_data()
    try:
        action = data["action"]
    except Exception as e:
        await callback.message.answer("Я потерял действие. Попробуйте еще раз.")
        print(e)
        return

    if prediction:
        await show_prediction(callback.bot, callback.message.chat.id, prediction)
    else:
        await callback.message.answer("Предсказание не найдено.")
        return
    
    if action == "delete":
        await callback.message.answer("Вы точно хотите удалить это предсказание? Я буду грустить🥺",
                                      reply_markup=await delete_confirm_kb())
    else:
        await callback.message.answer("Выберите что хотите отредактировать в предсказании:",
                                      reply_markup=await edit_prediction_fields_kb())
    
    
@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    await send_kb_to_admin(callback.message)