import redis.asyncio as redis
from typing import Optional
from src.config import settings


class RedisRepository:
    """Репозиторий для работы с Redis кешем"""
    
    # Время жизни ключей в Redis (6 часов = 21600 секунд)
    TTL_SECONDS = 60 * 2
    
    # Префиксы для ключей
    USER_PREFIX = "user:"
    ADMIN_PREFIX = "admin:"
    
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
        key = f"{self.USER_PREFIX}:{user_id}"
        await self.redis.setex(key, self.TTL_SECONDS, "1")
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
        key = f"{self.USER_PREFIX}:{user_id}"
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
    
    # ========== Методы для админов ==========

    async def add_admin(self, admin_id: int) -> bool:
        """
        Добавление ID админа в кеш для функции
        
        Args:
            admin_id: ID админа
            
        Returns:
            True, если операция успешна
        """
        await self.connect()
        key = f"{self.ADMIN_PREFIX}:{admin_id}"
        await self.redis.setex(key, self.TTL_SECONDS, "1")
        return True
    
    async def is_admin_exists(self, admin_id: int) -> bool:
        """
        Проверка, находится ли админ в кеше
        
        Args:
            admin_id: ID админа
            
        Returns:
            True, если админ находится в кеше
        """
        await self.connect()
        key = f"{self.ADMIN_PREFIX}:{admin_id}"
        result = await self.redis.exists(key)
        return result == 1
    
    
    

