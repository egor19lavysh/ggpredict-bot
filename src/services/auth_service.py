from src.config import settings
from src.repositories.redis_repository import RedisRepository


class AuthService:
    """Сервис аутентификации и авторизации"""
    
    def __init__(self, redis_repository: RedisRepository = None):
        self.redis_repository = redis_repository or RedisRepository()
    
    async def verify_admin_password(self, user_id: int, password: str) -> bool:
        """
        Проверка правильности пароля администратора
        
        Args:
            user_id: ID пользователя (для логирования)
            password: Введённый пароль
            
        Returns:
            True, если пароль верный, False иначе
        """
        return password == settings.ADMIN_PASSWORD
    
    async def authenticate_admin(self, user_id: int, password: str) -> bool:
        """
        Аутентификация админа: проверка пароля и добавление в Redis кэш
        
        Args:
            user_id: ID админа
            password: Введённый пароль
            
        Returns:
            True, если аутентификация успешна, False иначе
        """
        # Проверяем пароль
        if not await self.verify_admin_password(user_id, password):
            return False
        
        # Добавляем админа в кэш на 6 часов
        await self.redis_repository.add_admin(user_id)
        return True
    
    async def is_admin_authenticated(self, admin_id: int) -> bool:
        """
        Проверка, аутентифицирован ли админ
        
        Args:
            admin_id: ID админа
            
        Returns:
            True, если админ аутентифицирован, False иначе
        """
        return await self.redis_repository.is_admin_exists(admin_id)
