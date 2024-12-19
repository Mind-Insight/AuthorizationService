from sqlalchemy import Column, Integer, String
from db.database import Base


class User(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
