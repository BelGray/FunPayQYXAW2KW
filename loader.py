from aiogram.client.default import DefaultBotProperties

import bot_config_manager
from aiogram import Bot, Dispatcher

config = bot_config_manager.BotConfig()
telegram = config.telegram_token
admin = config.admin_id
tribute = config.tribute_link

bot = Bot(token=telegram, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
