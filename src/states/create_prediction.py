from aiogram.fsm.state import State, StatesGroup


class CreatePredictionStates(StatesGroup):
    text = State()
    image = State()
    status = State()
    chance = State()