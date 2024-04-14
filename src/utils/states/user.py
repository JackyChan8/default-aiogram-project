from aiogram.fsm.state import StatesGroup, State


class TestStates(StatesGroup):
    text = State()
    is_test = State()
