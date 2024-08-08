from datetime import datetime

from aiogram.client.default import DefaultBotProperties

import bot_config_manager
from aiogram import Bot, Dispatcher
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

config = bot_config_manager.BotConfig()
telegram = config.telegram_token
admin = config.admin_id
tribute = config.tribute_link

release_notes = {
    "version": "1.1",
    "date": datetime(year=2024, month=8, day=8)
}

bot = Bot(token=telegram, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
