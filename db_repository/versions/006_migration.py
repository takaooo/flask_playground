from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tk_User = Table('tk_User', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('social_id', VARCHAR(length=64), nullable=False),
    Column('nickname', VARCHAR(length=64), nullable=False),
    Column('email', VARCHAR(length=64)),
)

tk__user = Table('tk__user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('social_id', String(length=64), nullable=False),
    Column('nickname', String(length=64), nullable=False),
    Column('email', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tk_User'].drop()
    post_meta.tables['tk__user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tk_User'].create()
    post_meta.tables['tk__user'].drop()
