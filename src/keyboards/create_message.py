from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def create_message_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить сообщение✅", callback_data="create_message")],
        [InlineKeyboardButton(text="Удалить сообщение❌", callback_data="delete_message")],
        [InlineKeyboardButton(text="Редактировать сообщение✏️", callback_data="edit_message")]
    ])
    return keyboard


async def delete_confirm_kb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да✅", callback_data="confirm_да"), 
         InlineKeyboardButton(text="Нет❌", callback_data="confirm_нет")]
        ])
    return markup

async def edit_message_fields_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Текст", callback_data="edit_text")],
    ])
    return keyboard