from models.base import Base
from sqlalchemy import Column, BigInteger, Integer, String, Boolean

class Student(Base):
    __tablename__ = "students"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fullname = Column(String(50), nullable=False)
    age = Column(Integer)
    is_active = Column(Boolean, default=True)


