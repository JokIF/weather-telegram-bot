from sqlalchemy import Column, BigInteger, DECIMAL, ARRAY, String
from .user_table import RelateUser


class LocationUser(RelateUser):
    __tablename__ = 'user_loc'
    id = Column(BigInteger(), nullable=False, autoincrement=True, primary_key=True)
    lon = Column(DECIMAL, nullable=False)
    lat = Column(DECIMAL, nullable=False)
    address = Column(String(), nullable=False)
