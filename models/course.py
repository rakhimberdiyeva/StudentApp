from models.base import Base
from sqlalchemy import Column, BigInteger, Integer, String

class Course(Base):
    __tablename__ = "courses"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(String(500))
    duration_hours = Column(Integer, default=True)

