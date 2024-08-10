from aiogram.fsm.state import State, StatesGroup


class newList(StatesGroup):
    name = State()
    user_id = State()
    description = State()
    importance = State()
    condition = State()


class newTask(StatesGroup):
    name = State()
    user_id = State()
    parent_list = State()
    description = State()
    timeToComplete = State()
    importance = State()
    condition = State()