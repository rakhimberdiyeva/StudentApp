from models.base import Base
from sqlalchemy import Column, BigInteger, Integer, String, PrimaryKeyConstraint, ForeignKey


class Enrollment(Base):
    __tablename__ = "enrollments"
    student_id = Column(BigInteger, ForeignKey("students.id", ondelete="CASCADE"), primary_key=True)
    course_id = Column(BigInteger, ForeignKey("courses.id", ondelete="CASCADE"),primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint("student_id", "course_id"),
    )
