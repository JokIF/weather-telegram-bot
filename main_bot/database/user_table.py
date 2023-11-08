from gino import Gino
from sqlalchemy import Integer, String, Column, ForeignKey, BigInteger

db = Gino()


class User(db.Model):
    __tablename__ = 'user'
    id = Column(BigInteger(), nullable=False, autoincrement=False, primary_key=True)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=True)
    language = Column(String(), nullable=True)


class RelateUser(db.Model):
    __abstract__ = True
    user_id = Column(BigInteger(), ForeignKey(User.id), nullable=False)
