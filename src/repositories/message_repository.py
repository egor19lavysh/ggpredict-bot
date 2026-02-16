from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.models.message import Message


class MessageRepository:
    """Репозиторий для работы с предсказаниями"""

    @staticmethod
    async def create(
        text: str,
    ) -> Message:

        async with async_session_maker() as session:
            message = Message(
                text=text
            )
            session.add(message)
            await session.commit()
            await session.refresh(message)
            return message
    
    @staticmethod
    async def get_all() -> List[Message]:
        async with async_session_maker() as session:
            result = await session.execute(select(Message))
            return list(result.scalars().all())

    @staticmethod
    async def get_by_id(message_id: int) -> Optional[Message]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Message).where(Message.id == message_id)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def update_text(message_id: int, text: str) -> Optional[Message]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Message).where(Message.id == message_id)
            )
            message = result.scalar_one_or_none()
            if message:
                message.text = text
                await session.commit()
                await session.refresh(message)
            return message


    @staticmethod
    async def delete(message_id: int) -> bool:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Message).where(Message.id == message_id)
            )
            message = result.scalar_one_or_none()
            if message:
                await session.delete(message)
                await session.commit()
                return True
            return False
