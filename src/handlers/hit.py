import datetime
from time import time
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from src.exceptions import *
from aiogram.exceptions import TelegramBadRequest
from src.services.message_service import MessageService
from src.repositories.redis_repository import RedisRepository
from src.repositories.main_boss_repository import MainBossRepository
from src.utils.google_sheets_client import GoogleSheetsClient
from src.services.boss_service import BossService
from src.utils.time_utils import get_cooldown_message
from src.config import settings
from datetime import timedelta
import asyncio


router = Router()
message_service = MessageService()
redis_repository = RedisRepository()
boss_service = BossService()
main_boss_repository = MainBossRepository()
gs_client = GoogleSheetsClient(
    settings.CREDENTIALS,
    settings.SPREADSHEET_ID
    )

TEXT_MESSAGE = """
{user} нанес {damage} урона {boss} 💥

{message}

⏳До следующей попытки нанести урон: 3 часа
"""


@router.message(Command("hit"))
async def hit_command_handler(message: Message):
    try:
        msg, damage =await message_service.get_message_and_damage(user_id=message.from_user.id)

        if await redis_repository.is_main_boss_exists():
            main_boss_id = await redis_repository.get_main_boss_id()
        else:
            main_boss_id = await main_boss_repository.get_main_boss_id()
            if main_boss_id is not None:
                await redis_repository.save_main_boss_id(main_boss_id)

        boss = await boss_service.get_boss_by_id(main_boss_id)

        await message.reply(TEXT_MESSAGE.format(
            user=message.from_user.first_name if message.from_user.first_name else "Странник",
            damage=damage,
            boss=boss.name if boss else "главному боссу",
            message=msg.text))
        
        await gs_client.hit(
            user_info=[message.from_user.id, 
                       message.from_user.username if message.from_user.username else "Аноним", 
                       str(datetime.datetime.now() + timedelta(hours=3))],  # Сохраняем время следующей попытки
            boss_name=boss.name if boss else "Главный босс"
        )
        
    except MessageLimitExceeded:
        user_timestamp = await redis_repository.get_user(message.from_user.id)
        current_time = datetime.datetime.now() + timedelta(hours=3)  # Текущее время + 3 часа для корректного отображения
        time = await get_cooldown_message(user_timestamp, current_time)
        message_sent = await message.reply(f"Ты уже нанес урон главному боссу. ⏳До следующей попытки нанести урон: {time} часов")
        await asyncio.sleep(5)
        await message_sent.delete()
        await message.delete()
    except Exception as e:
        await message.reply("Произошла ошибка при попытке нанести урон главному боссу. Пожалуйста, попробуй снова позже.")
        print(f"Error in hit_command_handler: {e}")




        


