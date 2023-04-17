from aiogram import Dispatcher
from loguru import logger

from main_bot.filters.settings_word import SettingsWord
from main_bot.filters.weather_current_word import WeatherCurrentWord
from main_bot.filters.weather_history_word import WeatherHistoryWord


def setup(dp: Dispatcher):
    logger.info('filters setup')
    dp.filters_factory.bind(SettingsWord)
    dp.filters_factory.bind(WeatherCurrentWord)


__all__ = ['setup', 'SettingsWord', 'WeatherCurrentWord', 'WeatherHistoryWord']
