from typing import Optional, List
import random
from src.repositories.message_repository import MessageRepository
from src.repositories.redis_repository import RedisRepository
from src.models.message import Message
from src.exceptions import *



class MessageService:

    def __init__(self, repository: MessageRepository = None, redis_repository: RedisRepository = None):
        self.repository = repository or MessageRepository()
        self.redis_repository = redis_repository or RedisRepository()
    
    async def create_message(
        self,
        text: str
    ) -> Message:
        return await self.repository.create(
            text=text,
        )
    
    async def get_all_messages(self) -> List[Message]:
        return await self.repository.get_all()


    async def get_message_by_id(self, message_id: int) -> Optional[Message]:
        return await self.repository.get_by_id(message_id)
    
    async def update_message_text(
        self,
        message_id: int,
        text: str
    ) -> Optional[Message]:
        return await self.repository.update_text(message_id, text)
    
    async def delete_message(self, message_id: int) -> bool:
        return await self.repository.delete(message_id=message_id)
    
    async def get_random_message(self) -> Optional[Message]:
        messages = await self.get_all_messages()
        
        if not messages:
            return None
        
        selected_index = random.randint(0, len(messages) - 1)
        
        return messages[selected_index]
    
    
    async def get_message_and_damage(self, user_id: int) -> tuple[Message, int]:
        # Проверяем, есть ли пользователь в кэше
        user_exists = await self.redis_repository.is_user_exists(user_id)
        
        if user_exists:
            raise MessageLimitExceeded
        # Получаем предсказание
        message = await self.get_random_message()
        damage = random.randint(20, 1000)
        
        # Добавляем пользователя в кэш на 6 часов
        await self.redis_repository.add_user(user_id)
        
        return message, damage
