import asyncio
import random
from src.repositories.prediction_repository import PredictionRepository
from src.models.prediction import StatusEnum


async def update_acc():
    repository = PredictionRepository()
    
    preds = await repository.get_all()
    for pred in preds:
        await repository.update_accumulted(pred.id, 0.0)

if __name__ == "__main__":
    asyncio.run(update_acc())
