from aiogram.fsm.state import State, StatesGroup

class addVideoFreeModel(StatesGroup):
    addMessage = State()
    addURL = State()

class addVideo(StatesGroup):
    addMessage = State()
    addURL = State()

class setTestModel(StatesGroup):
    setTest = State()

class broadcastModel(StatesGroup):
    broadcast = State()