from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from src.models.prediction import Prediction


def predictions_keyboard(
    predictions: List[Prediction],
    current_page: int = 0,
    items_per_page: int = 2
) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры с предсказаниями (2 столбца по 9 предсказаний).
    
    Args:
        predictions: Список всех предсказаний
        current_page: Текущая страница (начиная с 0)
        items_per_page: Количество предсказаний на странице (по умолчанию 18)
        
    Returns:
        InlineKeyboardMarkup с предсказаниями и кнопками навигации
    """
    
    # Вычисляем диапазон предсказаний для текущей страницы
    start_idx = current_page * items_per_page
    end_idx = start_idx + items_per_page
    page_predictions = predictions[start_idx:end_idx]
    
    # Считаем общее количество страниц
    total_pages = (len(predictions) + items_per_page - 1) // items_per_page
    
    # Создаём клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    # Добавляем предсказания в 2 столбца (9 в каждом)
    for i in range(0, len(page_predictions), 2):
        row = []
        
        # Первое предсказание в строке
        pred_1 = page_predictions[i]
        row.append(InlineKeyboardButton(
            text=f"{pred_1.text[:20]}...",
            callback_data=f"prediction_{pred_1.id}"
        ))
        
        # Второе предсказание в строке (если есть)
        if i + 1 < len(page_predictions):
            pred_2 = page_predictions[i + 1]
            row.append(InlineKeyboardButton(
                text=f"{pred_2.text[:20]}...",
                callback_data=f"prediction_{pred_2.id}"
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
    if current_page > 0:
        navigation_row.append(InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=f"predictions_page_{current_page - 1}"
        ))
    
    # Кнопка "Вперед"
    if current_page < total_pages - 1:
        navigation_row.append(InlineKeyboardButton(
            text="Вперед ➡️",
            callback_data=f"predictions_page_{current_page + 1}"
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
