import asyncio
from src.repositories.boss_repository import BossRepository

boss_list = [
    "ЦЗЯНШИ",
    "ХУЛИ-ЦЗИН",
    "НЮТОУ",
    "ХРАНИТЕЛЬ РАЗЛОМА",
    "ТАОТЭ",
    "зал стихий",
    "БАЙХУ",
    "МОРСКОЙ СТРАЖ",
    "АО ГУАН",
    "Яньло-ван",
]


async def add_bosses_to_db():
    
    # Добавляем только новых боссов
    for boss_name in boss_list:
        await BossRepository.create(name=boss_name.lower().capitalize())

async def delete_bosses_from_db():
    bosses = await BossRepository.get_all()
    for boss in bosses:
        await BossRepository.delete(boss.id)

if __name__ == "__main__":
    asyncio.run(delete_bosses_from_db())
    asyncio.run(add_bosses_to_db())
