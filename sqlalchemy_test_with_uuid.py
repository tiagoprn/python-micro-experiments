# coding: utf-8
'''
    This code provides a user table, with an UUID being used instead of a classic auto-increment integer ID.
    It also uses an sqlite database memory as the storage engine.

    REFERENCE:
        http://silviud.blogspot.com.br/2011/02/sqlalchemy-uuid-as-primary-key.html

    CONSIDERATIONS:
        1) This UUID implementation is not meant to be used on "serious" production code.
        In this case, it will be better to user PostgreSQL which has a native UUID type.
        Here is how to use it with SQLAlchemy:
            http://docs.sqlalchemy.org/en/rel_0_9/dialects/postgresql.html#sqlalchemy.dialects.postgresql.UUID

        2) Using UUIDs  instead of regular INTEGER IDs makes you lose the feature to order by latest
        IDs, so it is nice to also have on your table a field name "created_at" with a timestamp
        (maybe unix timestamp?), to allow you to get the latest records on your database.
'''
from sqlalchemy import Table, Column, Integer, String, Sequence, MetaData, ForeignKey, CHAR
from sqlalchemy.orm import mapper, sessionmaker, scoped_session
from sqlalchemy import create_engine
import uuid

metadata = MetaData()

# The table as in the database
users = Table('users', metadata,
    Column('id', CHAR(32), primary_key=True, autoincrement=True),
    Column('first_name', String(50)),
    Column('last_name', String(50))
 )

# The SQLAlchemy ORM mapping
class Users(object):
    def __init__(self, first_name, last_name):
         assert isinstance(first_name, str), 'first_name is not a string'
         assert isinstance(last_name, str), 'last_name is not a string'
         self.first_name = first_name
         self.last_name = last_name

# maps the database table to the orm
# maps a temporary integer used by sqlalchemy and then you transform it into the UUID with 32 chars in hex.
mapper(Users, users, version_id_col=users.c.id, version_id_generator = lambda version:uuid.uuid4().hex)

# setups the orm to be used
engine = create_engine('sqlite:///:memory:', echo=False)
# engine = create_engine('sqlite:///tutorial.db', echo=True)
Session = scoped_session(sessionmaker(bind=engine))
metadata.drop_all(engine)
metadata.create_all(engine)

# here we make a test to verify all is OK
session = Session()
u = Users('s', 'd');
u1 = Users('s1', 'd2');
session.add_all([u1, u])
session.commit()
print "---"
all_users = session.query(Users).all()
for user in all_users:
    print "UUID: %s, first_name: %s, last_name: %s" % (user.id, user.first_name, user.last_name)
