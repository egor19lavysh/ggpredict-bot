from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from sqlalchemy import Integer



class Boss(Base):
    __tablename__ = "bosses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str]

class MainBoss(Base):
    __tablename__ = "main_boss"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    boss_id: Mapped[int]