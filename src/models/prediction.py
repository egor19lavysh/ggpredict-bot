from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from sqlalchemy import Integer, String
import enum


class StatusEnum(str, enum.Enum):
   LEGENDARY = "Легендарный"
   RARE = "Редкий"
   EPIC = "Эпический"
   STEAM_KEY = "Ключ игры Steam"
   WITHOUT_PRIZE = "Без приза"



class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str]
    image: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(default=StatusEnum.WITHOUT_PRIZE)
    chance: Mapped[float]