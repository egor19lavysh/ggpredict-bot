from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from src.services.message_service import MessageService
from src.keyboards.common import messages_keyboard
from src.keyboards.create_message import create_message_keyboard, delete_confirm_kb, edit_message_fields_kb
from aiogram.fsm.context import FSMContext
from src.models.message import Message
from aiogram.exceptions import TelegramBadRequest
from .auth import send_kb_to_admin


router = Router()
message_service = MessageService()

@router.callback_query(F.data == "messages")
async def list_messages(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Выберите действие:", reply_markup=await create_message_keyboard())


@router.callback_query(F.data.in_(("edit_message", "delete_message")))
async def edit_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    messages = await message_service.get_all_messages()

    await state.update_data(action=callback.data.split("_")[0])
    await callback.message.answer("Выберите сообщение:", reply_markup=messages_keyboard(messages))

@router.callback_query(F.data.startswith("messages_page_"))
async def show_messages_page(callback: CallbackQuery):
    await callback.answer()

    page = int(callback.data.split("_")[-1])
    messages = await message_service.get_all_messages()
    keyboard = messages_keyboard(messages, current_page=page)
    
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    

async def show_message(bot: Bot, chat_id: int, message: Message):
    message_text = f"Сообщение: {message.text}"
    await bot.send_message(
                chat_id,
                text=message_text
            )

@router.callback_query(F.data.startswith("message_"))
async def show_message_detail(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    
    message_id = int(callback.data.split("_")[-1])
    await state.update_data(message_id=message_id)
    message = await message_service.get_message_by_id(message_id)

    data = await state.get_data()
    try:
        action = data["action"]
    except Exception as e:
        await callback.message.answer("Я потерял действие. Попробуйте еще раз.")
        print(e)
        return

    if message:
        await show_message(callback.bot, callback.message.chat.id, message)
    else:
        await callback.message.answer("Сообщение не найдено.")
        return
    
    if action == "delete":
        await callback.message.answer("Вы точно хотите удалить это сообщение? Я буду грустить🥺",
                                      reply_markup=await delete_confirm_kb())
    else:
        await callback.message.answer("Выберите что хотите отредактировать в сообщении:",
                                      reply_markup=await edit_message_fields_kb())
    
    
@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    await send_kb_to_admin(callback.message)
    
    
@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    await send_kb_to_admin(callback.message)