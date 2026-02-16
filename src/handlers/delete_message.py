from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from src.services.message_service import MessageService
from .auth import send_kb_to_admin


router = Router()
message_service = MessageService()

@router.callback_query(F.data.startswith("confirm_"))
async def confirm_delete_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    choice = callback.data.split("_")[-1]
    data = await state.get_data()

    try:
        message_id = data["message_id"]
    except Exception as e:
        await callback.message.answer("Я потерял сообщение. Попробуйте еще раз.")

    if choice == "да":
        await message_service.delete_message(message_id=message_id)
        await callback.message.answer("Сообщение удалено. Я не плачу, это просто пиксели😭")
    else:
        await callback.message.answer("Удаление отменено.")

    await state.clear()

    await send_kb_to_admin(callback.message)

