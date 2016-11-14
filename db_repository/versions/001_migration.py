from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
app_user = Table('app_user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR),
)

test = Table('test', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('num', INTEGER),
    Column('data', VARCHAR),
)

transaction = Table('transaction', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('bank', VARCHAR(length=50)),
    Column('description', VARCHAR(length=100)),
    Column('amount', INTEGER),
    Column('transaction_date', TIMESTAMP),
    Column('user_id', INTEGER),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['app_user'].drop()
    pre_meta.tables['test'].drop()
    pre_meta.tables['transaction'].drop()
    pre_meta.tables['user'].columns['name'].drop()
    post_meta.tables['user'].columns['email'].create()
    post_meta.tables['user'].columns['nickname'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['app_user'].create()
    pre_meta.tables['test'].create()
    pre_meta.tables['transaction'].create()
    pre_meta.tables['user'].columns['name'].create()
    post_meta.tables['user'].columns['email'].drop()
    post_meta.tables['user'].columns['nickname'].drop()
