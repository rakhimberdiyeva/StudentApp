from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

STUDENTS = []
COURSES = []

class StudentCreate(BaseModel):
    id: int = Field(ge=1)
    full_name: str
    age: int = Field(ge=1)
    is_active: bool

class StudentPut(BaseModel):
    full_name: str
    age: int = Field(ge=1)
    is_active: bool

class StudentPatch(BaseModel):
    is_active: bool

class CourseCreate(BaseModel):
    id: int = Field(ge=1)
    title: str
    description: str
    duration: int = Field(ge=0)

class CoursePut(BaseModel):
    title: str
    description: str
    duration: int = Field(ge=0)

class CoursePatch(BaseModel):
    duration: int = Field(ge=0)

@app.post("/students")
async def create_student(request: StudentCreate):
    STUDENTS.append(request.model_dump())
    return {"success": True}

@app.get("/students")
async def get_students():
    return STUDENTS

@app.get("/students/{student_id}")
async def get_students(student_id: int= Path(ge=1)):
    for student in STUDENTS:
        if student_id == student["id"]:
            return student
    return None


@app.put("/students/{student_id}")
async def put_students(request: StudentPut, student_id: int= Path(ge=1)):
    for student in STUDENTS:
        if student_id == student["id"]:
            student["full_name"] = request.full_name
            student["age"] = request.age
            student["is_active"] = request.is_active
            return student
    return None


@app.patch("/students/{student_id}")
async def patch_students(request: StudentPatch, student_id: int= Path(ge=1)):
    for student in STUDENTS:
        if student_id == student["id"]:
            student["is_active"] = request.is_active
            return student
    return None

@app.delete("/students/{student_id}")
async def delete_students(request: StudentPatch, student_id: int= Path(ge=1)):
    for student in STUDENTS:
        if student_id == student["id"]:
            STUDENTS.remove(student)
    return None


################# 2
@app.post("/courses")
async def create_course(request: CourseCreate):
    COURSES.append(request.model_dump())
    return {"success": True}

@app.get("/courses")
async def get_course():
    return COURSES

@app.get("/courses/{course_id}")
async def get_courses(course_id: int= Path(ge=1)):
    for course in COURSES:
        if course_id == course["id"]:
            return course
    return None

@app.put("/courses/{course_id}")
async def put_courses(request: CoursePut, course_id: int= Path(ge=1)):
    for course in COURSES:
        if course_id == course["id"]:
            course["title"] = request.title
            course["description"] = request.description
            course["duration"] = request.duration
            return course
    return None

@app.patch("/courses/{course_id}")
async def patch_courses(request: CoursePatch, course_id: int= Path(ge=1)):
    for course in COURSES:
        if course_id == course["id"]:
            course["duration"] = request.duration
            return course
    return None


@app.delete("/courses/{course_id}")
async def delete_courses( course_id: int= Path(ge=1)):
    for course in COURSES:
        if course_id == course["id"]:
            COURSES.remove(course)
    return None

################## 3
@app.get("/students", summary="is active")
async def get_active_students(is_active: bool | None = Query(default=None)):
    for student in STUDENTS:
        if is_active == student["is_active"]:
            return student
    return None

@app.get("/students", summary="min age")
async def get_min_age(student_age: int | None = Query(default=None)):
    for student in STUDENTS:
        if student_age == student["age"]:
            return student
    return None