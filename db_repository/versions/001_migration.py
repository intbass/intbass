from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
roles = Table('roles', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
)

user_capabilities = Table('user_capabilities', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('userid', Integer),
    Column('capability', String(length=12)),
)

users = Table('users', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('pic', VARCHAR(length=250)),
    Column('email', VARCHAR(length=120)),
    Column('role', SMALLINT),
    Column('location', VARCHAR(length=64)),
    Column('password', VARCHAR(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['roles'].drop()
    post_meta.tables['user_capabilities'].create()
    pre_meta.tables['users'].columns['role'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['roles'].create()
    post_meta.tables['user_capabilities'].drop()
    pre_meta.tables['users'].columns['role'].create()
