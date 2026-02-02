from typing import Optional, List
import numpy as np
from src.repositories.prediction_repository import PredictionRepository
from src.repositories.redis_repository import RedisRepository
from src.models.prediction import Prediction, StatusEnum
from src.exceptions import PredictionLimitExceeded, PredictionNotFound
from aiogram import Bot
from src.utils.notify import notify_admins


class PredictionService:

    def __init__(self, repository: PredictionRepository = None, redis_repository: RedisRepository = None):
        self.repository = repository or PredictionRepository()
        self.redis_repository = redis_repository or RedisRepository()
    
    async def create_prediction(
        self,
        text: str,
        chance: float,
        image: Optional[str] = None,
        status: StatusEnum = StatusEnum.WITHOUT_PRIZE
    ) -> Prediction:
        """
        Создание нового предсказания
        
        Args:
            text: Текст предсказания
            chance: Шанс (вероятность)
            image: ID изображения
            status: Статус предсказания
            
        Returns:
            Созданный объект Prediction
        """
        return await self.repository.create(
            text=text,
            chance=chance,
            image=image,
            status=status
        )
    
    async def get_all_predictions(self) -> List[Prediction]:
        """
        Получение всех предсказаний
        
        Returns:
            Список всех предсказаний
        """
        return await self.repository.get_all()
    
    async def get_unusual_predictions(self) -> List[Prediction]:
        predicitions = await self.get_all_predictions()
        unusual_predictions = []
        for prediction in predicitions:
            if prediction.status != StatusEnum.WITHOUT_PRIZE:
                unusual_predictions.append(prediction)
        return unusual_predictions

    async def get_prediction_by_id(self, prediction_id: int) -> Optional[Prediction]:
        """
        Получение предсказания по ID
        
        Args:
            prediction_id: ID предсказания
            
        Returns:
            Объект Prediction или None, если не найдено
        """
        return await self.repository.get_by_id(prediction_id)
    
    async def update_prediction_text(
        self,
        prediction_id: int,
        text: str
    ) -> Optional[Prediction]:
        """
        Изменение текста предсказания
        
        Args:
            prediction_id: ID предсказания
            text: Новый текст
            
        Returns:
            Обновленный объект Prediction или None, если не найдено
        """
        return await self.repository.update_text(prediction_id, text)
    
    async def update_prediction_image(
        self,
        prediction_id: int,
        image: Optional[str]
    ) -> Optional[Prediction]:
        """
        Изменение изображения предсказания
        
        Args:
            prediction_id: ID предсказания
            image: Новое изображение
            
        Returns:
            Обновленный объект Prediction или None, если не найдено
        """
        return await self.repository.update_image(prediction_id, image)
    
    async def update_prediction_status(
        self,
        prediction_id: int,
        status: StatusEnum
    ) -> Optional[Prediction]:
        """
        Изменение статуса предсказания
        
        Args:
            prediction_id: ID предсказания
            status: Новый статус
            
        Returns:
            Обновленный объект Prediction или None, если не найдено
        """
        return await self.repository.update_status(prediction_id, status)
    
    async def update_prediction_chance(
        self,
        prediction_id: int,
        chance: float
    ) -> Optional[Prediction]:
        """
        Изменение шанса предсказания
        
        Args:
            prediction_id: ID предсказания
            chance: Новый шанс
            
        Returns:
            Обновленный объект Prediction или None, если не найдено
        """
        return await self.repository.update_chance(prediction_id, chance)
    
    async def update_prediction_accumulted(
            self,
            prediction_id: int,
            value: float
    ) -> Optional[Prediction]:
        return await self.repository.update_accumulted(prediction_id=prediction_id, value=value)
    
    async def reset_predictions_accumulated(self) -> None:
        predictions = await self.get_unusual_predictions()
        for prediction in predictions:
            await self.update_prediction_accumulted(prediction_id=prediction.id, value=0)

    async def add_to_prediction_accumulted(
            self,
            prediction_id: int,
            value: float
    ) -> Optional[Prediction]:
        if prediction := await self.get_prediction_by_id(prediction_id=prediction_id):
            return await self.update_prediction_accumulted(prediction_id=prediction_id, value=prediction.accumulated + value)
        return None
    
    async def add_unusual_predictions_accumulated(self, value: float = 0.01) -> None:
        predictions = await self.get_unusual_predictions()
        for prediction in predictions:
            await self.add_to_prediction_accumulted(prediction_id=prediction.id, value=value)

    
    async def delete_prediction(self, prediction_id: int) -> bool:
        """
        Удаление предсказания по ID
        
        Args:
            prediction_id: ID предсказания
            
        Returns:
            True, если удаление успешно, False иначе
        """
        return await self.repository.delete(prediction_id)
    
    async def get_random_prediction(self) -> Optional[Prediction]:
        """
        Получение случайного предсказания на основе вероятностей (chance)
        
        Returns:
            Случайное предсказание или None, если предсказаний нет
        """
        predictions = await self.get_all_predictions()
        
        if not predictions:
            return None
        
        # Извлекаем шансы
        chances = np.array([prediction.chance + prediction.accumulated for prediction in predictions])
        
        # Нормализуем шансы в вероятности (сумма = 1)
        probabilities = chances / chances.sum()
        
        # Выбираем случайный индекс на основе вероятностей
        selected_index = np.random.choice(len(predictions), p=probabilities)
        
        return predictions[selected_index]
    
    async def _get_prediction(self, bot: Bot, user_id: int) -> Optional[Prediction]:
        """
        Получение случайного предсказания с проверкой статуса.
        Если статус не обычный (не WITHOUT_PRIZE), то предсказание удаляется из БД.
        
        Returns:
            Случайное предсказание со статусом WITHOUT_PRIZE или None
        """
        prediction = await self.get_random_prediction()
        
        if prediction is None:
            return None
        
        # Если статус не обычный (не без приза), удаляем предсказание
        if prediction.status != StatusEnum.WITHOUT_PRIZE:
            await notify_admins(bot=bot, user_id=user_id, status=prediction.status)
            await self.delete_prediction(prediction.id)
            await self.reset_predictions_accumulated()
        else:
            await self.add_unusual_predictions_accumulated()
        
        return prediction
    
    async def get_prediction(self, user_id: int, bot: Bot) -> Prediction:
        """
        Получение случайного предсказания для пользователя с проверкой лимитов.
        Пользователь может получать предсказания не чаще чем раз в 6 часов.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Случайное предсказание
            
        Raises:
            PredictionLimitExceeded: Если пользователь превысил лимит запросов
            PredictionNotFound: Если нет доступных предсказаний
        """
        # Проверяем, есть ли пользователь в кэше
        user_exists = await self.redis_repository.is_user_exists(user_id)
        
        if user_exists:
            raise PredictionLimitExceeded(
                f"Вы уже получали предсказание. Попробуйте позже."
            )
        
        # Получаем предсказание
        prediction = await self._get_prediction(bot=bot, user_id=user_id)
        
        # Добавляем пользователя в кэш на 6 часов
        await self.redis_repository.add_user(user_id)
        
        return prediction
