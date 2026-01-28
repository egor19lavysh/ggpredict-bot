from aiogram.fsm.state import State, StatesGroup


class EditPredictionStates(StatesGroup):
    text = State()
    image = State()
    status = State()
    chance = State()
