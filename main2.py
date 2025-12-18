from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

from schemas.course import CourseCreate, CoursePut, CoursePatch
from views.course import c_create, c_read_all, c_read, c_edit, c_edit_partial, c_remove
from views.enrollment import e_create, e_read_all, e_read, e_read_courses, e_remove
from views.student import create, read, read_all, edit, edit_partial, remove, s_deactivate
from schemas.student import StudentCreate, StudentPut, StudentPatch

app = FastAPI()

@app.post("/students")
async def create_student(request: StudentCreate):
    response = await create(request)
    return response

@app.get("/students")
async def get_students(
        is_active: bool | None = Query(default=None),
        min_age: int | None = Query(default=None)
):
        response = await read_all(is_active, min_age)
        return response


@app.get("/students/{student_id}")
async def get_students(student_id: int= Path(ge=1)):
    response = await read(student_id)
    return response


@app.put("/students/{student_id}")
async def put_students(request: StudentPut, student_id: int= Path(ge=1)):
    response = await edit(student_id, request)
    return response


@app.patch("/students/{student_id}")
async def patch_students(request: StudentPatch, student_id: int= Path(ge=1)):
    response = await edit_partial(student_id, request)
    return response

@app.delete("/students/{student_id}")
async def delete_students(student_id: int= Path(ge=1)):
    response = await remove(student_id)
    return response



@app.post("/courses")
async def create_course(request: CourseCreate):
    response = await c_create(request)
    return response

@app.get("/courses")
async def get_course(
        title: str | None = Query(default=None),
        description: str | None = Query(default=None)
):
    response = await c_read_all(title, description)
    return response


@app.get("/courses/{course_id}")
async def get_courses(course_id: int= Path(ge=1)):
    response = await c_read(course_id)
    return response

@app.put("/courses/{course_id}")
async def put_courses(request: CoursePut, course_id: int= Path(ge=1)):
    response = await c_edit(course_id, request)
    return response

@app.patch("/courses/{course_id}")
async def patch_courses(request: CoursePatch, course_id: int= Path(ge=1)):
    response = await c_edit_partial(course_id, request)
    return response


@app.delete("/courses/{course_id}")
async def delete_courses( course_id: int= Path(ge=1)):
    response = await c_remove(course_id)
    return response


@app.post("/students/{student_id}/courses/{course_id}")
async def enroll(student_id: int, course_id: int):
    response = await e_create(student_id, course_id)
    return response




@app.get("/enrollments")
async def get_enrollments():
    response = await e_read_all()
    return response


@app.get("/students/{student_id}/courses")
async def get_student_courses(student_id: int):
    response = await e_read(student_id)
    return response


@app.get("/courses/{course_id}/students")
async def get_courses_students(course_id: int):
    response = await e_read_courses(course_id)
    return response


@app.delete('/students/{student_id}/courses/{course_id}')
async def delete_student_from_course(student_id: int, course_id: int):
    response = await e_remove(student_id, course_id)
    return response


@app.post("/students/{student_id}/deactivate")
async def deactivate(student_id: int):
    response = await s_deactivate(student_id)
    return response