from aiogram import Router, F
from aiogram.types import Message
from src.services.prediction_service import PredictionService
from aiogram.filters import Command
from src.exceptions import *
from src.models.prediction import Prediction
from aiogram.exceptions import TelegramBadRequest
import asyncio


router = Router()
prediction_service = PredictionService()


async def send_prediction(message: Message, prediction: Prediction, message_id: int):
    if prediction.image:
        try:
            await message.answer_photo(photo=prediction.image, caption=prediction.text, reply_to_message_id=message_id)
        except TelegramBadRequest:
            await message.answer_animation(animation=prediction.image, caption=prediction.text, reply_to_message_id=message_id)
        except Exception as e:
            await message.answer(prediction.text, reply_to_message_id=message_id)
            print(e)
    else:
        await message.answer(prediction.text, reply_to_message_id=message_id)


@router.message(Command("pred"))
async def pred_cmd(message: Message):
    try:
        prediction = await prediction_service.get_prediction(user_id=message.from_user.id,
                                               bot=message.bot)
        await send_prediction(message=message, prediction=prediction, message_id=message.message_id)
    except PredictionLimitExceeded as e:
        msg = await message.answer(e.message, reply_to_message_id=message.message_id)
        await asyncio.sleep(10)
        await msg.delete()
    except Exception as e:
        await message.answer("Произошла какая-то ошибка... Попробуйте позже", reply_to_message_id=message.message_id)
        print(e)