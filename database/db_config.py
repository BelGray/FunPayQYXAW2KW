import sqlalchemy as db

eng = db.create_engine('sqlite:///bot.db', echo=True)
conn = eng.connect()
meta = db.MetaData()

users = db.Table('users', meta,
            db.Column('telegram_id', db.Integer),
            db.Column('used', db.Boolean)
)

meta.create_all(eng, checkfirst=True)
