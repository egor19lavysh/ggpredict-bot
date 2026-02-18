from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column

# Костыль, чтобы включать/выключать босса

class BossAlive(Base):
    __tablename__ = "boss_alive"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_alive: Mapped[bool] = mapped_column(default=False)
