from aiogram.dispatcher.filters.state import State, StatesGroup


class StartStates(StatesGroup):
    start = State()


class SettingsStates(StatesGroup):
    setting = State()
    select_loc = State()
    select_lang = State()


class WeatherStates(StatesGroup):
    current_weather = State()
    history = State()
