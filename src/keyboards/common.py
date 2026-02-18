from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from typing import List
from src.models.message import Message


def messages_keyboard(
    messages: List[Message],
    current_page: int = 0,
    items_per_page: int = 18
) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры с сообщениями (2 столбца по 9 сообщений).
    
    Args:
        messages: Список всех сообщений
        current_page: Текущая страница (начиная с 0)
        items_per_page: Количество сообщений на странице (по умолчанию 18)
        
    Returns:
        InlineKeyboardMarkup с сообщениями и кнопками навигации
    """
    
    # Вычисляем диапазон предсказаний для текущей страницы
    start_idx = current_page * items_per_page
    end_idx = start_idx + items_per_page
    page_messages = messages[start_idx:end_idx]
    
    # Считаем общее количество страниц
    total_pages = (len(messages) + items_per_page - 1) // items_per_page
    
    # Создаём клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    # Добавляем сообщения в 2 столбца (9 в каждом)
    for i in range(0, len(page_messages), 2):
        row = []
        
        # Первое сообщение в строке
        msg_1 = page_messages[i]
        row.append(InlineKeyboardButton(
            text=f"{msg_1.text[:20]}...",
            callback_data=f"message_{msg_1.id}"
        ))
        
        # Второе сообщение в строке (если есть)
        if i + 1 < len(page_messages):
            msg_2 = page_messages[i + 1]
            row.append(InlineKeyboardButton(
                text=f"{msg_2.text[:20]}...",
                callback_data=f"message_{msg_2.id}"
            ))
        
        keyboard.inline_keyboard.append(row)
    
    # Кнопка показывающая номер страницы
    page_button_row = [InlineKeyboardButton(
        text=f"Страница {current_page + 1}/{total_pages}",
        callback_data="blank"
    )]
    keyboard.inline_keyboard.append(page_button_row)
    
    # Кнопки навигации (назад, вперед)
    navigation_row = []
    
    # Кнопка "Назад"
    navigation_row.append(InlineKeyboardButton(
            text="⬅️Назад",
            callback_data=f"messages_page_{current_page - 1}" if current_page > 0 else "blank"
        ))
    
    # Кнопка "Вперед" 
    navigation_row.append(InlineKeyboardButton(
            text="Вперед➡️",
            callback_data=f"messages_page_{current_page + 1}" if current_page < total_pages - 1 else "blank"
        ))
    
    if navigation_row:
        keyboard.inline_keyboard.append(navigation_row)
    
    # Кнопка "Обратно" для удаления клавиатуры
    back_row = [InlineKeyboardButton(
        text="🔙 Обратно",
        callback_data="back_to_menu"
    )]
    keyboard.inline_keyboard.append(back_row)
    
    return keyboard

def get_back_kb() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой 'Назад'."""
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Назад")]
    ], resize_keyboard=True)
    return keyboard

def get_entities_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сообщения", callback_data="messages")],
        [InlineKeyboardButton(text="Боссы", callback_data="bosses")],
        [InlineKeyboardButton(text="Активировать/деактивировать босса", callback_data="control_boss")]
    ])
    return keyboard