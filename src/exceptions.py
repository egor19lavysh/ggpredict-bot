"""Кастомные исключения приложения"""


class PredictionLimitExceeded(Exception):
    """Исключение, выбрасываемое когда лимит предсказаний исчерпан"""
    def __init__(self, message: str = "Лимит предсказаний исчерпан. Попробуйте позже."):
        self.message = message
        super().__init__(self.message)


class PredictionNotFound(Exception):
    """Исключение, выбрасываемое когда предсказание не найдено"""
    def __init__(self, message: str = "Нет доступных предсказаний"):
        self.message = message
        super().__init__(self.message)
