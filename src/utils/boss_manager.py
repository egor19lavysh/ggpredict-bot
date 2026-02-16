from src.repositories.main_boss_repository import MainBossRepository


async def save_main_boss_id(boss_id: int) -> bool:
    """
    Сохраняет ID главного босса в базу данных
    
    Args:
        boss_id: ID главного босса
        
    Returns:
        True, если операция успешна
    """
    await MainBossRepository.set_main_boss(boss_id)
    return True


async def get_main_boss_id() -> int | None:
    """
    Получает ID главного босса из базы данных
    
    Returns:
        ID главного босса или None, если его нет
    """
    return await MainBossRepository.get_main_boss_id()


async def is_main_boss_exists() -> bool:
    """
    Проверяет, объявлен ли главный босс
    
    Returns:
        True, если главный босс объявлен
    """
    main_boss_id = await MainBossRepository.get_main_boss_id()
    return main_boss_id is not None


async def remove_main_boss() -> bool:
    """
    Удаляет главного босса из базы данных
    
    Returns:
        True, если операция успешна
    """
    return await MainBossRepository.delete_main_boss()
