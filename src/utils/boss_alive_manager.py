from sqlalchemy import select
from src.database import async_session_maker
from src.models.boss_alive import BossAlive
from src.repositories.redis_repository import RedisRepository


redis_repo = RedisRepository()


async def create_boss_alive_controller():
    async with async_session_maker() as session:
        # Если запись уже есть — возвращаем её, иначе создаём первую запись
        result = await session.execute(
            select(BossAlive).where(BossAlive.id == 1)
        )
        boss = result.scalar_one_or_none()
        if boss:
            # Обновляем кеш в Redis на случай, если его нет или устарел
            await redis_repo.save_boss_alive(boss.is_alive)
            return boss

        boss = BossAlive(is_alive=False)
        session.add(boss)
        await session.commit()
        await session.refresh(boss)
        await redis_repo.save_boss_alive(boss.is_alive)
        return boss
    
async def update_boss_alive_controller(is_alive: bool):
    async with async_session_maker() as session:
        result = await session.execute(
            select(BossAlive).where(BossAlive.id == 1)
        )
        boss = result.scalar_one_or_none()
        if boss:
            boss.is_alive = is_alive
            await session.commit()
            await session.refresh(boss)
            await redis_repo.save_boss_alive(boss.is_alive)
            return boss

        # Если записи нет — создаём её с нужным статусом
        boss = BossAlive(is_alive=is_alive)
        session.add(boss)
        await session.commit()
        await session.refresh(boss)
        await redis_repo.save_boss_alive(boss.is_alive)
        return boss
    
async def get_boss_alive_controller():
    async with async_session_maker() as session:
        result = await session.execute(
            select(BossAlive).where(BossAlive.id == 1)
        )
        boss = result.scalar_one_or_none()
        # Если записи ещё нет — создаём её (по умолчанию неактивна)
        if boss:
            return boss

        boss = BossAlive(is_alive=False)
        session.add(boss)
        await session.commit()
        await session.refresh(boss)
        await redis_repo.save_boss_alive(boss.is_alive)
        return boss
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(create_boss_alive_controller())