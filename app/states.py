from aiogram.fsm.state import State, StatesGroup


class newList(StatesGroup):
    name = State()
    type = State()
    description = State()
    condition = State()


class newTask(StatesGroup):
    name = State()
    description = State()
    timeToComplete = State()
    condition = State()