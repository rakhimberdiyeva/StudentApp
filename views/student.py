from fastapi import Response
from sqlalchemy import select, insert, delete, update
from session import async_session
from models.student import Student
from schemas.student import StudentCreate, StudentPut, StudentPatch

async def create(
        request: StudentCreate
):
    stmt = insert(Student).values(
        fullname=request.fullname,
        age=request.age,
        is_active=request.is_active
    )

    async with async_session() as session:
        await session.execute(stmt)
        await session.commit()

    return {
        "status": "success"
    }


async def read(
        student_id: int
):
    stmt = select(Student).where(student_id == Student.id)

    async with async_session() as session:
        result = await session.execute(stmt)
        student = result.scalar_one_or_none()
        if not student:
            return None
    return student



async def read_all(
        is_active: bool | None,
        min_age: int | None
):
    stmt = select(Student)
    async with async_session() as session:
        result = await session.execute(stmt)
        students = result.scalars().all()


    if is_active is not None:
        students = [student for student in students if is_active == student.is_active]

    if min_age is not None:
        students = [student for student in students if min_age <= student.age]

    return students


async def edit(
        student_id: int,
        request: StudentPut
):
    student = await read(student_id)
    if isinstance(student, Response):
        return student

    stmt = update(Student).values(
        fullname=request.fullname,
        age=request.age,
        is_active=request.is_active
    ).where(student_id == Student.id)

    async with async_session() as session:
        await session.execute(stmt)
        await session.commit()

    return {
        "status": "success"
    }


async def edit_partial(
        student_id: int,
        request: StudentPatch
):
    student = await read(student_id)
    if isinstance(student, Response):
        return student

    stmt = update(Student).values(
        is_active=request.is_active
    ).where(student_id == Student.id)

    async with async_session() as session:
        await session.execute(stmt)
        await session.commit()

    return {
        "status": "success"
    }


async def remove(
        student_id: int
):
    stmt = delete(Student).where(student_id == Student.id)

    async with async_session() as session:
        await session.execute(stmt)
        await session.commit()

    return {
        "status": "success"
    }


async def s_deactivate(
        student_id: int,
):
    student = await read(student_id)
    if isinstance(student, Response):
        return student

    stmt = update(Student).values(
        is_active=False
    ).where(student_id == Student.id)

    async with async_session() as session:
        await session.execute(stmt)
        await session.commit()

    return {
        "status": "success"
    }