from sqlalchemy import Column, Integer, TIMESTAMP, String

from .user_table import RelateUser

import datetime


class UserImages(RelateUser):
    __tablename__ = "user_images"
    id = Column(Integer(), nullable=False, autoincrement=True, primary_key=True)
    url = Column(String(), nullable=False)
    create_at = Column(TIMESTAMP, nullable=False)

