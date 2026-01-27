from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def create_prediction_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить предсказание✅", callback_data="create_prediction")],
        [InlineKeyboardButton(text="Удалить предсказание❌", callback_data="delete_prediction")],
        [InlineKeyboardButton(text="Редактировать предсказание✏️", callback_data="edit_prediction")]
    ])
    return keyboard

async def skip_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пропустить⏩", callback_data="skip_image")]
    ])
    return keyboard

async def status_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Легендарный", callback_data="status_Легендарный"), InlineKeyboardButton(text="Редкий", callback_data="status_Редкий")],
        [InlineKeyboardButton(text="Эпический", callback_data="status_Эпический"), InlineKeyboardButton(text="Ключ игры Steam", callback_data="status_Ключ игры Steam")],
        [InlineKeyboardButton(text="Без приза", callback_data="status_Без приза")],
    ])
    return keyboard