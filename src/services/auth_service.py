from sqlalchemy import select
from src.config import settings
from src.models.admin import Admin
from src.repositories.redis_repository import RedisRepository
from src.database import async_session_maker


class AuthService:
    """Сервис аутентификации и авторизации"""
    
    def __init__(self, redis_repository: RedisRepository = None):
        self.redis_repository = redis_repository or RedisRepository()

    async def get_admins(self) -> list[int]:
        """Получение списка ID администраторов из базы данных"""
        async with async_session_maker() as session:
            result = await session.execute(
                select(Admin)
            )
            return [admin.user_id for admin in result.scalars().all()]
        
    async def is_admin_authenticated(self, user_id: int) -> bool:
        """Проверка, аутентифицирован ли админ (по наличию в базе данных)"""
        admins = await self.get_admins()
        return user_id in admins
    
    async def verify_admin_password(self, password: str) -> bool:
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
        if not await self.verify_admin_password(password):
            return False
        
        async with async_session_maker() as session:
            admin = Admin(
                user_id=user_id
            )
            session.add(admin)
            await session.commit()
        
        return True