from aiogram import Router, F
from aiogram.types import CallbackQuery
from src.handlers.auth import send_kb_to_admin
from src.keyboards.control_boss import control_boss_keyboard 
from src.utils.boss_alive_manager import get_boss_alive_controller, update_boss_alive_controller


router = Router()

@router.callback_query(F.data == "control_boss")
async def control_boss_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()

    boss_alive = await get_boss_alive_controller()
    if boss_alive is None:
        await callback_query.message.answer("Ошибка: статус босса не найден.")
        return
    
    await callback_query.message.answer(
        text=f"Текущий статус босса: {'Активен' if boss_alive.is_alive else 'Неактивен'}",
        reply_markup=control_boss_keyboard())
    

@router.callback_query(F.data.in_(("activate_boss", "deactivate_boss")))
async def toggle_boss_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()

    is_activating = callback_query.data == "activate_boss"
    new_status = await update_boss_alive_controller(is_alive=is_activating)

    if new_status is None:
        await callback_query.message.answer("Ошибка: не удалось обновить статус босса.")
        return
    
    await callback_query.message.answer(
        text=f"Босс теперь {'Активен' if new_status.is_alive else 'Неактивен'}")
    
    await send_kb_to_admin(callback_query.message)