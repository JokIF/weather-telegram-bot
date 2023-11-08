from sqlalchemy import Column, BigInteger, TIMESTAMP, String

from .user_table import RelateUser


class UserImages(RelateUser):
    __tablename__ = "user_images"
    id = Column(BigInteger(), nullable=False, autoincrement=True, primary_key=True)
    url = Column(String(), nullable=False)
    create_at = Column(TIMESTAMP, nullable=False)

