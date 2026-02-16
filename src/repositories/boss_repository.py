from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.models.boss import Boss


class BossRepository:
    """Репозиторий для работы с боссами"""

    @staticmethod
    async def create(name: str) -> Boss:
        async with async_session_maker() as session:
            boss = Boss(name=name)
            session.add(boss)
            await session.commit()
            await session.refresh(boss)
            return boss
    
    @staticmethod
    async def get_all() -> List[Boss]:
        async with async_session_maker() as session:
            result = await session.execute(select(Boss))
            return list(result.scalars().all())

    @staticmethod
    async def get_by_id(boss_id: int) -> Optional[Boss]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Boss).where(Boss.id == boss_id)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def update(boss_id: int, name: str) -> Optional[Boss]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Boss).where(Boss.id == boss_id)
            )
            boss = result.scalar_one_or_none()
            if boss:
                boss.name = name
                await session.commit()
                await session.refresh(boss)
            return boss

    @staticmethod
    async def delete(boss_id: int) -> bool:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Boss).where(Boss.id == boss_id)
            )
            boss = result.scalar_one_or_none()
            if boss:
                await session.delete(boss)
                await session.commit()
                return True
            return False
