from loader import admin


class Admin:
    __admin = admin

    @staticmethod
    async def is_admin(user_telegram_id: int) -> bool:
        return int(admin) == int(user_telegram_id)
