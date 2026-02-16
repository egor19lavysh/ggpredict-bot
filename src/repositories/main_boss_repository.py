from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.models.boss import MainBoss


class MainBossRepository:
    """Репозиторий для работы с главным боссом"""

    @staticmethod
    async def set_main_boss(boss_id: int) -> MainBoss:
        """
        Устанавливает главного босса (удаляет старого и добавляет нового)
        
        Args:
            boss_id: ID босса
            
        Returns:
            Объект MainBoss
        """
        async with async_session_maker() as session:
            # Удаляем существующего главного босса
            await session.execute(select(MainBoss))
            result = await session.execute(select(MainBoss))
            existing = result.scalar_one_or_none()
            
            if existing:
                await session.delete(existing)
            
            # Добавляем нового главного босса
            main_boss = MainBoss(boss_id=boss_id)
            session.add(main_boss)
            await session.commit()
            await session.refresh(main_boss)
            return main_boss
    
    @staticmethod
    async def get_main_boss() -> Optional[MainBoss]:
        """
        Получает текущего главного босса
        
        Returns:
            Объект MainBoss или None
        """
        async with async_session_maker() as session:
            result = await session.execute(select(MainBoss))
            return result.scalar_one_or_none()
    
    @staticmethod
    async def get_main_boss_id() -> Optional[int]:
        """
        Получает ID главного босса
        
        Returns:
            ID босса или None
        """
        async with async_session_maker() as session:
            result = await session.execute(select(MainBoss))
            main_boss = result.scalar_one_or_none()
            return main_boss.boss_id if main_boss else None
    
    @staticmethod
    async def delete_main_boss() -> bool:
        """
        Удаляет главного босса
        
        Returns:
            True, если был удален главный босс
        """
        async with async_session_maker() as session:
            result = await session.execute(select(MainBoss))
            main_boss = result.scalar_one_or_none()
            
            if main_boss:
                await session.delete(main_boss)
                await session.commit()
                return True
            return False
