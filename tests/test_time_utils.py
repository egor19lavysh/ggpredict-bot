import datetime
import pytest
from src.utils.time_utils import get_cooldown_message


class TestGetCooldownMessage:
    """Тесты для функции get_cooldown_message"""
    
    def test_returns_none_when_timestamp_is_none(self):
        """Функция должна вернуть None если timestamp_str равен None"""
        current_time = datetime.datetime(2026, 2, 16, 12, 0, 0)
        result = get_cooldown_message(None, current_time)
        assert result is None
    
    def test_returns_none_when_timestamp_is_empty_string(self):
        """Функция должна вернуть None если timestamp_str пустая строка"""
        current_time = datetime.datetime(2026, 2, 16, 12, 0, 0)
        result = get_cooldown_message("", current_time)
        assert result is None
    
    def test_returns_none_on_invalid_timestamp_format(self):
        """Функция должна вернуть None если timestamp в неправильном формате"""
        current_time = datetime.datetime(2026, 2, 16, 12, 0, 0)
        result = get_cooldown_message("invalid_timestamp", current_time)
        assert result is None
    
    def test_returns_none_on_malformed_timestamp(self):
        """Функция должна вернуть None если timestamp не парсится"""
        current_time = datetime.datetime(2026, 2, 16, 12, 0, 0)
        result = get_cooldown_message("2026-02-16 not_a_time", current_time)
        assert result is None
    
    def test_cooldown_expired_message(self):
        """Функция должна вернуть сообщение о том, что кулдаун закончился"""
        last_hit_time = datetime.datetime(2026, 2, 16, 9, 0, 0)
        current_time = datetime.datetime(2026, 2, 16, 13, 0, 0)  # 4 часа спустя
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "Готово! Ты можешь нанести урон"
    
    def test_cooldown_expired_at_exact_time(self):
        """Функция должна вернуть сообщение о том, что кулдаун закончился ровно в момент истечения"""
        last_hit_time = datetime.datetime(2026, 2, 16, 9, 0, 0)
        current_time = datetime.datetime(2026, 2, 16, 12, 0, 0)  # ровно 3 часа спустя
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "Готово! Ты можешь нанести урон"
    
    def test_remaining_time_1_hour(self):
        """Функция должна вернуть сообщение с 1 часом (правильное склонение)"""
        last_hit_time = datetime.datetime(2026, 2, 16, 9, 0, 0)
        current_time = datetime.datetime(2026, 2, 16, 11, 0, 0)  # 2 часа спустя
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: 1 час"
    
    def test_remaining_time_2_hours(self):
        """Функция должна вернуть сообщение с 2 часами (правильное склонение)"""
        last_hit_time = datetime.datetime(2026, 2, 16, 9, 0, 0)
        current_time = datetime.datetime(2026, 2, 16, 10, 0, 0)  # 1 час спустя
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: 2 часа"
    
    def test_remaining_time_5_hours(self):
        """Функция должна вернуть сообщение с 5 часами (правильное склонение)"""
        last_hit_time = datetime.datetime(2026, 2, 16, 9, 0, 0)
        # next_hit_time = 12:00:00, осталось 5 часов значит current_time = 07:00:00
        current_time = datetime.datetime(2026, 2, 16, 7, 0, 0)
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: 5 часов"
    
    def test_remaining_time_21_hours(self):
        """Функция должна вернуть сообщение с 21 часом (правильное склонение)"""
        last_hit_time = datetime.datetime(2026, 2, 16, 9, 0, 0)
        # next_hit_time = 12:00:00, осталось 21 час значит current_time = 15:00:00 предыдущего дня
        current_time = datetime.datetime(2026, 2, 15, 15, 0, 0)
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: 21 час"
    
    def test_remaining_time_less_than_minute(self):
        """Функция должна вернуть сообщение о менее минуте"""
        last_hit_time = datetime.datetime(2026, 2, 16, 8, 59, 45)
        # next_hit_time = 11:59:45, осталось 30 секунд значит current_time = 11:59:15
        current_time = datetime.datetime(2026, 2, 16, 11, 59, 15)
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: менее минуты"
    
    def test_remaining_time_1_minute(self):
        """Функция должна вернуть сообщение с 1 минутой (правильное склонение)"""
        last_hit_time = datetime.datetime(2026, 2, 16, 8, 58, 0)
        # next_hit_time = 11:58:00, осталось 1 минута значит current_time = 11:57:00
        current_time = datetime.datetime(2026, 2, 16, 11, 57, 0)
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: 1 минута"
    
    def test_remaining_time_2_minutes(self):
        """Функция должна вернуть сообщение с 2 минутами (правильное склонение)"""
        last_hit_time = datetime.datetime(2026, 2, 16, 8, 57, 0)
        # next_hit_time = 11:57:00, осталось 2 минуты значит current_time = 11:55:00
        current_time = datetime.datetime(2026, 2, 16, 11, 55, 0)
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: 2 минуты"
    
    def test_remaining_time_5_minutes(self):
        """Функция должна вернуть сообщение с 5 минутами (правильное склонение)"""
        last_hit_time = datetime.datetime(2026, 2, 16, 8, 54, 0)
        # next_hit_time = 11:54:00, осталось 5 минут значит current_time = 11:49:00
        current_time = datetime.datetime(2026, 2, 16, 11, 49, 0)
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: 5 минут"
    
    def test_remaining_time_21_minutes(self):
        """Функция должна вернуть сообщение с 21 минутой (правильное склонение)"""
        last_hit_time = datetime.datetime(2026, 2, 16, 8, 38, 0)
        # next_hit_time = 11:38:00, осталось 21 минута значит current_time = 11:17:00
        current_time = datetime.datetime(2026, 2, 16, 11, 17, 0)
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: 21 минута"
    
    def test_only_minutes_no_hours(self):
        """Функция должна показать только минуты, если осталось менее часа"""
        last_hit_time = datetime.datetime(2026, 2, 16, 11, 30, 0)
        # next_hit_time = 14:30:00, осталось 30 минут значит current_time = 14:00:00
        current_time = datetime.datetime(2026, 2, 16, 14, 0, 0)
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: 30 минут"
    
    def test_with_microseconds(self):
        """Функция должна корректно работать с микросекундами в timestamp"""
        last_hit_time = datetime.datetime(2026, 2, 16, 9, 0, 0, 123456)
        # next_hit_time = 12:00:00.123456, осталось 1 час значит current_time = 11:00:00.123456
        current_time = datetime.datetime(2026, 2, 16, 11, 0, 0, 123456)
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: 1 час"
    
    def test_different_dates(self):
        """Функция должна корректно работать при переходе через границу дней"""
        last_hit_time = datetime.datetime(2026, 2, 15, 23, 0, 0)
        # next_hit_time = 2026-02-16 02:00:00, осталось 0 значит current_time >= 2026-02-16 02:00:00
        current_time = datetime.datetime(2026, 2, 16, 2, 30, 0)  # прошло 3 часа
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "Готово! Ты можешь нанести урон"
    
    def test_edge_case_30_seconds(self):
        """Функция должна вернуть 'менее минуты' при 30 секундах оставшегося времени"""
        last_hit_time = datetime.datetime(2026, 2, 16, 11, 59, 30)
        # next_hit_time = 14:59:30, осталось 30 секунд значит current_time = 14:59:00
        current_time = datetime.datetime(2026, 2, 16, 14, 59, 0)
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: менее минуты"
    
    def test_edge_case_59_seconds(self):
        """Функция должна вернуть 'менее минуты' при 59 секундах оставшегося времени"""
        last_hit_time = datetime.datetime(2026, 2, 16, 11, 59, 1)
        # next_hit_time = 14:59:01, осталось 59 секунд значит current_time = 14:58:02
        current_time = datetime.datetime(2026, 2, 16, 14, 58, 2)
        
        result = get_cooldown_message(last_hit_time.isoformat(), current_time)
        assert result == "До следующей попытки: менее минуты"


class TestGetHourForm:
    """Тесты для функции-помощника _get_hour_form"""
    
    def test_hour_forms(self):
        """Проверяет правильное склонение слова 'час'"""
        from src.utils.time_utils import _get_hour_form
        
        # 1 час
        assert _get_hour_form(1) == "час"
        assert _get_hour_form(21) == "час"
        assert _get_hour_form(31) == "час"
        
        # 2-4 часа
        assert _get_hour_form(2) == "часа"
        assert _get_hour_form(3) == "часа"
        assert _get_hour_form(4) == "часа"
        assert _get_hour_form(22) == "часа"
        assert _get_hour_form(23) == "часа"
        
        # 5-20, 25-30 часов
        assert _get_hour_form(5) == "часов"
        assert _get_hour_form(6) == "часов"
        assert _get_hour_form(20) == "часов"
        assert _get_hour_form(25) == "часов"
        
        # Исключения (11-19)
        assert _get_hour_form(11) == "часов"
        assert _get_hour_form(12) == "часов"
        assert _get_hour_form(13) == "часов"
        assert _get_hour_form(14) == "часов"


class TestGetMinuteForm:
    """Тесты для функции-помощника _get_minute_form"""
    
    def test_minute_forms(self):
        """Проверяет правильное склонение слова 'минута'"""
        from src.utils.time_utils import _get_minute_form
        
        # 1 минута
        assert _get_minute_form(1) == "минута"
        assert _get_minute_form(21) == "минута"
        assert _get_minute_form(31) == "минута"
        
        # 2-4 минуты
        assert _get_minute_form(2) == "минуты"
        assert _get_minute_form(3) == "минуты"
        assert _get_minute_form(4) == "минуты"
        assert _get_minute_form(22) == "минуты"
        assert _get_minute_form(23) == "минуты"
        
        # 5-20, 25-30 минут
        assert _get_minute_form(5) == "минут"
        assert _get_minute_form(6) == "минут"
        assert _get_minute_form(20) == "минут"
        assert _get_minute_form(25) == "минут"
        
        # Исключения (11-19)
        assert _get_minute_form(11) == "минут"
        assert _get_minute_form(12) == "минут"
        assert _get_minute_form(13) == "минут"
        assert _get_minute_form(14) == "минут"
