from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.models.boss import Boss


def boss_keyboard(bosses: list[Boss]) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для боссов.
    
    Returns:
        InlineKeyboardMarkup с кнопками для каждого босса
    """
    
    keyboard = InlineKeyboardBuilder()
    
    for boss in bosses:
        keyboard.add(InlineKeyboardButton(text=boss.name, callback_data=f"boss_{boss.id}"))

    keyboard.adjust(2)

    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="back_to_menu"))
    
    return keyboard.as_markup()

def select_boss_keyboard(boss_id: int) -> InlineKeyboardMarkup:
    
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(InlineKeyboardButton(text="Выбрать главным боссом", callback_data=f"select_boss_{boss_id}"))

    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="back_to_menu"))
    
    return keyboard.as_markup()