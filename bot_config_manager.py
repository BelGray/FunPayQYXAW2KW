import atexit
import enum
import os
import pickle
from BGLogger import BGC


class BotConfigError(Exception):
    """Ошибка при настройке конфигурации бота"""
    pass


class BotConfigKeys(enum.Enum):
    TELEGRAM_API_TOKEN = "telegram_api_token"
    ADMIN_ID = "admin_id"


class BotConfig:
    """Сохранение конфигурации бота для быстрого перезапуска. (Сериализация и десериализация данных)"""

    def __init__(self):

        self.__bytes_file: str = 'bot_config.pickle'

        if not os.path.exists(self.__bytes_file):
            with open(self.__bytes_file, 'wb') as file:
                serializable = {
                    BotConfigKeys.TELEGRAM_API_TOKEN.value: None,
                    BotConfigKeys.ADMIN_ID.value: None
                }
                pickle.dump(serializable, file)

        with open(self.__bytes_file, 'rb') as bytes_file:
            data = pickle.load(bytes_file)
            self.__telegram_token = data[BotConfigKeys.TELEGRAM_API_TOKEN.value]
            self.__admin_id = data[BotConfigKeys.ADMIN_ID.value]

        if self.__telegram_token is not None and self.__admin_id is not None:
            reset = BGC.scan(
                'Сбросить текущую конфигурацию бота (Telegram API токен, ID админа) ?\nY - Да, настроить всё заново\n<Enter> - Нет, запустить бота с текущей конфигурацией\n\n/> ',
                label_color=BGC.Color.MUSTARD
            )
            if reset.upper() == 'Y':
                self.__telegram_token = self.set_telegram_token()
                self.__admin_id = self.set_admin_id()
            else:
                pass
        else:
            self.__telegram_token = self.get_telegram_token()
            self.__admin_id = self.get_admin_id()
        atexit.register(self.__dump_config)

    @property
    def telegram_token(self):
        return self.__telegram_token

    @property
    def admin_id(self):
        return self.__admin_id

    def __dump_config(self):
        with open(self.__bytes_file, 'wb') as file:
            serializable = {
                BotConfigKeys.TELEGRAM_API_TOKEN.value: self.__telegram_token,
                BotConfigKeys.ADMIN_ID.value: self.__admin_id
            }
            pickle.dump(serializable, file)

    def __read_config(self):
        with open(self.__bytes_file, 'rb') as bytes_file:
            data = pickle.load(bytes_file)
            return data

    def get_telegram_token(self) -> str:
        token = self.__read_config()[BotConfigKeys.TELEGRAM_API_TOKEN.value]
        if token is not None:
            return token
        new_token = BGC.scan('Telegram API токен (Получить можно в https://t.me/BotFather. Без токена бот банально не сможет взаимодействовать с Telegram) /> ', label_color=BGC.Color.CRIMSON)
        return new_token

    def get_admin_id(self) -> str:
        id = self.__read_config()[BotConfigKeys.ADMIN_ID.value]
        if id is not None:
            return id
        new_id = BGC.scan('Ваш Telegram ID (цифровое значение вида 1234567890, которое можно получить в боте https://t.me/username_to_id_bot. Ваш ID нужен чтобы у вас был доступ к скрытому функционалу) /> ', label_color=BGC.Color.CRIMSON)
        return new_id

    @classmethod
    def set_telegram_token(cls) -> str:
        new_token = BGC.scan('Telegram API токен (Получить можно в https://t.me/BotFather. Без токена бот банально не сможет взаимодействовать с Telegram) /> ', label_color=BGC.Color.CRIMSON)
        return new_token

    @classmethod
    def set_admin_id(cls) -> str:
        new_id = BGC.scan('Ваш Telegram ID (цифровое значение вида 1234567890, которое можно получить в боте https://t.me/username_to_id_bot. Ваш ID нужен чтобы у вас был доступ к скрытому функционалу) /> ', label_color=BGC.Color.CRIMSON)
        return new_id