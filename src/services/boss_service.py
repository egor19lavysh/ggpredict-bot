from typing import Optional, List
from src.repositories.boss_repository import BossRepository
from src.repositories.main_boss_repository import MainBossRepository
from src.models.boss import Boss
from src.repositories.redis_repository import RedisRepository


class BossService:

    def __init__(self, repository: BossRepository = None):
        self.repository = repository or BossRepository()
        self.redis_repository = RedisRepository()
    
    async def create_boss(self, name: str) -> Boss:
        return await self.repository.create(name=name)
    
    async def get_all_bosses(self) -> List[Boss]:
        return await self.repository.get_all()

    async def get_boss_by_id(self, boss_id: int) -> Optional[Boss]:
        return await self.repository.get_by_id(boss_id)
    
    async def update_boss(self, boss_id: int, name: str) -> Optional[Boss]:
        return await self.repository.update(boss_id, name)
    
    async def delete_boss(self, boss_id: int) -> bool:
        return await self.repository.delete(boss_id=boss_id)
    
    async def select_boss_as_main(self, boss_id: int) -> bool:
        """Выбрать босса в качестве главного."""
        # Заглушка для выбора главного босса
        res = await MainBossRepository.set_main_boss(boss_id)
        if res:
            await self.redis_repository.save_main_boss_id(boss_id=boss_id)
            return True
        return False