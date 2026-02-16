import datetime
from typing import Optional


def get_cooldown_message(timestamp_str: Optional[str], current_time: datetime.datetime) -> Optional[str]:
    """
    Получает сообщение об оставшемся времени до следующей попытки нанести урон
    
    Args:
        timestamp_str: Строка с временем последнего удара (из Redis)
        current_time: Текущее время
        
    Returns:
        Строка с сообщением об оставшемся времени, или None если timestamp_str None
    """
    if not timestamp_str:
        return None
    
    try:
        # Парсим timestamp из строки
        last_hit_time = datetime.datetime.fromisoformat(timestamp_str)
    except (ValueError, AttributeError):
        return None
    
    # Время до следующей попытки - 3 часа
    cooldown_duration = datetime.timedelta(hours=3)
    next_hit_time = last_hit_time + cooldown_duration
    
    # Вычисляем оставшееся время
    remaining_time = next_hit_time - current_time
    
    # Если время истекло
    if remaining_time.total_seconds() <= 0:
        return "Готово! Ты можешь нанести урон"
    
    # Преобразуем оставшееся время в часы и минуты
    total_seconds = remaining_time.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    
    # Если есть часы, возвращаем часы
    if hours > 0:
        return f"До следующей попытки: {hours} {_get_hour_form(hours)}"
    
    # Если только минуты
    if minutes > 0:
        return f"До следующей попытки: {minutes} {_get_minute_form(minutes)}"
    
    return "До следующей попытки: менее минуты"


def _get_hour_form(count: int) -> str:
    """
    Возвращает правильную форму слова 'час'
    
    Args:
        count: Количество часов
        
    Returns:
        Правильная форма слова 'час'
    """
    if count % 10 == 1 and count % 100 != 11:
        return "час"
    elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
        return "часа"
    else:
        return "часов"


def _get_minute_form(count: int) -> str:
    """
    Возвращает правильную форму слова 'минута'
    
    Args:
        count: Количество минут
        
    Returns:
        Правильная форма слова 'минута'
    """
    if count % 10 == 1 and count % 100 != 11:
        return "минута"
    elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
        return "минуты"
    else:
        return "минут"
