from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.models.prediction import Prediction, StatusEnum


class PredictionRepository:
    """Репозиторий для работы с предсказаниями"""

    @staticmethod
    async def create(
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
            image: id изображения
            status: Статус предсказания (по умолчанию WITHOUT_PRIZE)
            
        Returns:
            Созданный объект Prediction
        """
        async with async_session_maker() as session:
            prediction = Prediction(
                text=text,
                chance=chance,
                image=image,
                status=status
            )
            session.add(prediction)
            await session.commit()
            await session.refresh(prediction)
            return prediction

    @staticmethod
    async def get_all() -> List[Prediction]:
        """
        Получение всех предсказаний
        
        Returns:
            Список всех предсказаний
        """
        async with async_session_maker() as session:
            result = await session.execute(select(Prediction))
            return list(result.scalars().all())

    @staticmethod
    async def get_by_id(prediction_id: int) -> Optional[Prediction]:
        """
        Получение предсказания по ID
        
        Args:
            prediction_id: ID предсказания
            
        Returns:
            Объект Prediction или None, если не найдено
        """
        async with async_session_maker() as session:
            result = await session.execute(
                select(Prediction).where(Prediction.id == prediction_id)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def update_text(prediction_id: int, text: str) -> Optional[Prediction]:
        """
        Изменение текста предсказания
        
        Args:
            prediction_id: ID предсказания
            text: Новый текст
            
        Returns:
            Обновленный объект Prediction или None, если не найдено
        """
        async with async_session_maker() as session:
            result = await session.execute(
                select(Prediction).where(Prediction.id == prediction_id)
            )
            prediction = result.scalar_one_or_none()
            if prediction:
                prediction.text = text
                await session.commit()
                await session.refresh(prediction)
            return prediction

    @staticmethod
    async def update_image(prediction_id: int, image: Optional[str]) -> Optional[Prediction]:
        """
        Изменение изображения предсказания
        
        Args:
            prediction_id: ID предсказания
            image: Новый id изображения
            
        Returns:
            Обновленный объект Prediction или None, если не найдено
        """
        async with async_session_maker() as session:
            result = await session.execute(
                select(Prediction).where(Prediction.id == prediction_id)
            )
            prediction = result.scalar_one_or_none()
            if prediction:
                prediction.image = image
                await session.commit()
                await session.refresh(prediction)
            return prediction

    @staticmethod
    async def update_status(prediction_id: int, status: StatusEnum) -> Optional[Prediction]:
        """
        Изменение статуса предсказания
        
        Args:
            prediction_id: ID предсказания
            status: Новый статус
            
        Returns:
            Обновленный объект Prediction или None, если не найдено
        """
        async with async_session_maker() as session:
            result = await session.execute(
                select(Prediction).where(Prediction.id == prediction_id)
            )
            prediction = result.scalar_one_or_none()
            if prediction:
                prediction.status = status
                await session.commit()
                await session.refresh(prediction)
            return prediction

    @staticmethod
    async def update_chance(prediction_id: int, chance: float) -> Optional[Prediction]:
        """
        Изменение шанса предсказания
        
        Args:
            prediction_id: ID предсказания
            chance: Новый шанс (вероятность)
            
        Returns:
            Обновленный объект Prediction или None, если не найдено
        """
        async with async_session_maker() as session:
            result = await session.execute(
                select(Prediction).where(Prediction.id == prediction_id)
            )
            prediction = result.scalar_one_or_none()
            if prediction:
                prediction.chance = chance
                await session.commit()
                await session.refresh(prediction)
            return prediction

    @staticmethod
    async def delete(prediction_id: int) -> bool:
        """
        Удаление предсказания по ID
        
        Args:
            prediction_id: ID предсказания
            
        Returns:
            True, если предсказание было удалено, False если не найдено
        """
        async with async_session_maker() as session:
            result = await session.execute(
                select(Prediction).where(Prediction.id == prediction_id)
            )
            prediction = result.scalar_one_or_none()
            if prediction:
                await session.delete(prediction)
                await session.commit()
                return True
            return False
