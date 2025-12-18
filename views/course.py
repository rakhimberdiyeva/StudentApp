from wsgiref.util import request_uri

from fastapi import Response
from sqlalchemy import select, insert, delete, update
from session import async_session
from models.course import Course
from schemas.course import CourseCreate, CoursePatch, CoursePut

async def c_create(
        request: CourseCreate
):
    stmt = insert(Course).values(
        title=request.title,
        description=request.description,
        duration_hours=request.duration_hours
    )

    async with async_session() as session:
        await session.execute(stmt)
        await session.commit()

    return {
        "status": "success"
    }


async def c_read(
        course_id: int
):
    stmt = select(Course).where(course_id == Course.id)

    async with async_session() as session:
        result = await session.execute(stmt)
        course = result.scalar_one_or_none()
        if not course:
            return None

    return course


async def c_read_all(
        title: str | None,
        description: str | None
    ):
    stmt = select(Course)
    async with async_session() as session:
        result = await session.execute(stmt)
        courses = result.scalars().all()


    if title is not None:
        courses = [course for course in courses if course.title == title]

    if description is not None:
        courses = [course for course in courses if course.description == description]

    return courses

async def c_edit(
        course_id: int,
        request: CoursePut
):
    course = await c_read(course_id)
    if isinstance(course, Response):
        return course

    stmt = update(Course).values(
        title=request.title,
        description=request.description,
        duration_hours=request.duration_hours
    ).where(course_id == Course.id)
    async with async_session() as session:
        await session.execute(stmt)
        await session.commit()

    return {
        "status": "success"
    }


async def c_edit_partial(
        course_id: int,
        request: CoursePatch
):
    course = await c_read(course_id)
    if isinstance(course, Response):
        return course

    stmt = update(Course).values(
        duration_hours=request.duration_hours
    ).where(course_id == Course.id)

    async with async_session() as session:
        await session.execute(stmt)
        await session.commit()

    return {
        "status": "success"
    }


async def c_remove(
        course_id: int
):
    stmt = delete(Course).where(course_id == Course.id)

    async with async_session() as session:
        await session.execute(stmt)
        await session.commit()

    return {
        "status": "success"
    }