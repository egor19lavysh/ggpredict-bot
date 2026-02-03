from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def create_prediction_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить предсказание✅", callback_data="create_prediction")],
        [InlineKeyboardButton(text="Удалить предсказание❌", callback_data="delete_prediction")],
        [InlineKeyboardButton(text="Редактировать предсказание✏️", callback_data="edit_prediction")]
    ])
    return keyboard

async def skip_kb(with_back: bool = False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пропустить⏩", callback_data="skip_image")]
    ])
    
    if with_back:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="skip_back")])
    
    return keyboard

async def status_kb(with_back: bool = False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Легендарный", callback_data="status_Легендарный"), InlineKeyboardButton(text="Редкий", callback_data="status_Редкий")],
        [InlineKeyboardButton(text="Эпический", callback_data="status_Эпический"), InlineKeyboardButton(text="Ключ игры Steam", callback_data="status_Ключ игры Steam")],
        [InlineKeyboardButton(text="Без приза", callback_data="status_Без приза")],
    ])
    
    if with_back:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="status_back")])
    
    return keyboard

async def delete_confirm_kb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да✅", callback_data="confirm_да"), 
         InlineKeyboardButton(text="Нет❌", callback_data="confirm_нет")]
        ])
    return markup

async def edit_prediction_fields_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Текст", callback_data="edit_text")],
        [InlineKeyboardButton(text="Изображение", callback_data="edit_image")],
        [InlineKeyboardButton(text="Статус", callback_data="edit_status")],
        [InlineKeyboardButton(text="Шанс", callback_data="edit_chance")],
        [InlineKeyboardButton(text="Назад", callback_data="edit_back")],
    ])
    return keyboard