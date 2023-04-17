from gino import Gino
from sqlalchemy import Integer, String, Column, ForeignKey

db = Gino()


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer(), nullable=False, autoincrement=False, primary_key=True)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=True)
    language = Column(String(), nullable=True)


class RelateUser(db.Model):
    __abstract__ = True
    user_id = Column(Integer, ForeignKey(User.id), unique=True, nullable=False)
