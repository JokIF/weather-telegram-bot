from aiogram.fsm.state import StatesGroup, State


class StartStates(StatesGroup):
    start = State()


class SettingsStates(StatesGroup):
    setting = State()
    select_loc = State()
    select_lang = State()


class WeatherStates(StatesGroup):
    current_weather = State()
    history = State()
