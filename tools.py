import sqlalchemy as db

import database.db_config as tables
from database.db_config import conn


async def user_register(telegram_object):
    user_query = conn.execute(
        db.select(tables.users).where(tables.users.columns.telegram_id.like(telegram_object.from_user.id))
    )
    user = user_query.fetchall()
    if len(user) == 0:
        conn.execute(
            tables.users.insert().values([
                {
                    'telegram_id': telegram_object.from_user.id,
                    'used': False
                }
            ])
        )
        conn.commit()
