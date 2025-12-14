from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

STUDENTS = [
    {
      "id": 1,
      "full_name": "string",
      "age": 1,
      "is_active": True
    },
    {
        "id": 2,
        "full_name": "string",
        "age": 1,
        "is_active": True
    }
]
COURSES = [
    {
      "id": 1,
      "title": "string",
      "description": "string",
      "duration": 0
    },
    {
      "id": 2,
      "title": "string",
      "description": "string",
      "duration": 0
    }
]
ENROLLMENTS = [
    {
        "student_id": 1,
        "course_id": 1
    },
    {
        "student_id": 1,
        "course_id": 2
    },
    {
        "student_id": 2,
        "course_id": 1
    }
]

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

class EnrollmentsCreate(BaseModel):
    id: str = Field(ge=1)
    student_id: int = Field(ge=1)
    course_id: int = Field(ge=1)

@app.post("/students")
async def create_student(request: StudentCreate):
    STUDENTS.append(request.model_dump())
    return {"success": True}

# @app.get("/students")
# async def get_students():
#     return STUDENTS

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


# @app.patch("/students/{student_id}")
# async def patch_students(request: StudentPatch, student_id: int= Path(ge=1)):
#     for student in STUDENTS:
#         if student_id == student["id"]:
#             student["is_active"] = request.is_active
#             return student
#     return None

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

# @app.get("/courses")
# async def get_course():
#     return COURSES

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
@app.get("/students")
async def get_students(
        is_active: bool | None = Query(default=None),
        min_age: int | None = Query(default=None)
):
    result = STUDENTS
    if is_active is not None:
        result = [student for student in result if is_active == student["is_active"]]


    if min_age is not None:
        result = [student for student in result if min_age <= student["age"]]

    return result

#################### 4
@app.get("/courses")
async def get_course(
        title: str | None = Query(default=None),
        description: str | None = Query(default=None)
):
    result = COURSES

    if title is not None:
        result = [course for course in result if course["title"] == title]

    if description is not None:
        result = [course for course in result if course["description"] == description]

    return result

###################### 5
@app.post("/students/{student_id}/courses/{course_id}")
async def enroll(student_id: int, course_id: int):
    student = next((student for student in STUDENTS if student_id == student["id"]), None)
    if student is None:
        return {"message": "error"}
    course = next((course for course in COURSES if course_id == course["id"]), None)
    if course is None:
        return {"message": "error"}
    enrolled = [enrollment for enrollment in ENROLLMENTS if (enrollment["student_id"] == student_id and enrollment["course_id"] == course_id)]
    if not enrolled:
        ENROLLMENTS.append({"student_id": student_id, "course_id": course_id})
    return ENROLLMENTS



@app.get("/enrollments")
async def get_enrollments():
    return ENROLLMENTS

###################### 6
@app.get("/students/{student_id}/courses")
async def get_student_courses(student_id: int):
    result = [enrollment  for enrollment in ENROLLMENTS if student_id == enrollment["student_id"]]
    return result

###################### 7
@app.get("/courses/{course_id}/students")
async def get_courses_students(course_id: int):
    result = [enrollment for enrollment in ENROLLMENTS if course_id == enrollment["course_id"]]
    return result

###################### 8
@app.delete('/students/{student_id}/courses/{course_id}')
async def delete_student_from_course(student_id: int, course_id: int):
    student = next((student for student in STUDENTS if student_id == student["id"]), None)
    if student is None:
        return {"message": "error"}
    course = next((course for course in COURSES if course_id == course["id"]), None)
    if course is None:
        return {"message": "error"}
    enrolled = [enrollment for enrollment in ENROLLMENTS if (enrollment["student_id"] == student_id and enrollment["course_id"] == course_id)]
    if enrolled:
        for e in enrolled:
            ENROLLMENTS.remove(e)
    return ENROLLMENTS


###################### 9
@app.post("/students/{student_id}/deactivate")
async def deactivate(student_id: int):
    student = next((student for student in STUDENTS if student_id == student["id"]), None)
    if student["is_active"] == True:
        student["is_active"] = False
    return student

