from aiogram.fsm.state import State, StatesGroup


class Photo(StatesGroup):
    count = State()
    photo_id = State()
