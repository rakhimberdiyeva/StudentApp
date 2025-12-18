from sqlalchemy import select, insert, delete, update
from models.enrollment import Enrollment
from schemas.enrollment import EnrollmentCreate
from session import async_session

from views.student import read
from views.course import c_read


async def e_create(student_id: int, course_id:int):
    student = await read(student_id)
    if not student:
        return {
            "status": "error"
        }
    course = await read(course_id)
    if not course:
        return {
            "status": "error"
        }
    stmt = insert(Enrollment).values(
        student_id=student_id,
        course_id=course_id
    )

    async with async_session() as session:
        await session.execute(stmt)
        await session.commit()

    return {
        "status": "success"
    }


async def e_read_all():
    stmt = select(Enrollment)
    async with async_session() as session:
        result = await session.execute(stmt)
        return result.scalars().all()


async def e_read(
        student_id: int
):
    enrollments = await e_read_all()
    result = [enrollment for enrollment in enrollments if student_id == enrollment.student_id]
    return result


async def e_read_courses(course_id: int):
    enrollments = await e_read_all()
    result = [enrollment for enrollment in enrollments if course_id == enrollment.course_id]
    return result


async def e_remove(
        student_id: int,
        course_id: int
):
    student = await read(student_id)
    if not student:
        return {
            "status": "error"
        }
    course = await read(course_id)
    if not course:
        return {
            "status": "error"
        }

    stmt = delete(Enrollment).where(student_id == Enrollment.student_id and course_id == Enrollment.course_id)

    async with async_session() as session:
        await session.execute(stmt)
        await session.commit()

    return {
        "status": "success"
    }