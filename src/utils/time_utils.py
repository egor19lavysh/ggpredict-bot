import datetime
from typing import Optional


async def get_cooldown_message(timestamp_str: Optional[str], current_time: datetime.datetime) -> Optional[str]:
    """
    Получает оставшееся время до следующей попытки нанести урон в формате часы:минуты
    
    Args:
        timestamp_str: Строка с временем последнего удара (из Redis)
        current_time: Текущее время
        
    Returns:
        Строка формата "H:MM" (например "1:52"), или None если timestamp_str None
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
    
    # Если время истекло, возвращаем 0:00
    if remaining_time.total_seconds() <= 0:
        return "0:00"
    
    # Преобразуем оставшееся время в часы и минуты
    total_seconds = remaining_time.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    
    # Возвращаем в формате H:MM
    return f"{hours}:{minutes:02d}"
