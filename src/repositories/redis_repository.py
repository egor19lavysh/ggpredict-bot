import time
import redis.asyncio as redis
from typing import Optional
from src.config import settings
import datetime


class RedisRepository:
    """Репозиторий для работы с Redis кешем"""
    
    # Время жизни ключей в Redis (6 часов = 21600 секунд)
    TTL_SECONDS = 60
    # Время жизни главного босса (12 часов = 43200 секунд)
    MAIN_BOSS_TTL = 43200
    # Префикс для ключа главного босса
    MAIN_BOSS_KEY = "main_boss_id" 
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis = redis_client
    
    async def connect(self):
        """Подключение к Redis"""
        if not self.redis:
            self.redis = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf8",
                decode_responses=True
            )
    
    async def disconnect(self):
        """Отключение от Redis"""
        if self.redis:
            await self.redis.close()
    
    # ========== Методы для обычных пользователей ==========
    
    async def add_user(self, user_id: int) -> bool:
        """
        Добавление ID пользователя в кеш для функции
        
        Args:
            user_id: ID пользователя
            
        Returns:
            True, если операция успешна
        """
        await self.connect()
        key = f"{user_id}"
        timestamp = datetime.datetime.now()
        await self.redis.setex(key, self.TTL_SECONDS, str(timestamp))
        return True
    
    async def is_user_exists(self, user_id: int) -> bool:
        """
        Проверка, находится ли пользователь в кеше
        
        Args:
            user_id: ID пользователя
            
        Returns:
            True, если пользователь находится в кеше
        """
        await self.connect()
        key = f"{user_id}"
        result = await self.redis.exists(key)
        return result == 1

    async def remove_user(self, user_id: int) -> bool:
        """
        Удаление пользователя из кеша
        
        Args:
            user_id: ID пользователя
            
        Returns:
            True, если операция успешна
        """
        await self.connect()
        key = f"{self.USER_PREFIX}:{user_id}"
        await self.redis.delete(key)
        return True
    
    async def get_user(self, user_id: int) -> Optional[str]:
        """
        Получает время добавления пользователя
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Время добавления пользователя или None, если пользователя нет в кеше
        """
        await self.connect()
        key = f"{user_id}"
        timestamp = await self.redis.get(key)
        return timestamp
    
    # ========== Методы для управления главным боссом ==========
    
    async def save_main_boss_id(self, boss_id: int) -> bool:
        """
        Сохраняет ID главного босса в Redis на 12 часов
        
        Args:
            boss_id: ID главного босса
            
        Returns:
            True, если операция успешна
        """
        await self.connect()
        if await self.is_main_boss_exists():
            await self.remove_main_boss()
        await self.redis.setex(self.MAIN_BOSS_KEY, self.MAIN_BOSS_TTL, str(boss_id))
        return True
    
    async def get_main_boss_id(self) -> int | None:
        """
        Получает ID главного босса из Redis
        
        Returns:
            ID главного босса или None, если его нет в кеше
        """
        await self.connect()
        boss_id = await self.redis.get(self.MAIN_BOSS_KEY)
        return int(boss_id) if boss_id else None
    
    async def is_main_boss_exists(self) -> bool:
        """
        Проверяет, объявлен ли главный босс
        
        Returns:
            True, если главный босс объявлен
        """
        await self.connect()
        result = await self.redis.exists(self.MAIN_BOSS_KEY)
        return result == 1
    
    async def remove_main_boss(self) -> bool:
        """
        Удаляет главного босса из кеша
        
        Returns:
            True, если операция успешна
        """
        await self.connect()
        await self.redis.delete(self.MAIN_BOSS_KEY)
        return True
