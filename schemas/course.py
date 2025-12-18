from pydantic import BaseModel, Field

class CourseBase(BaseModel):
    title: str
    description: str
    duration_hours: int = Field(ge=0)

class CourseCreate(CourseBase):
    pass

class CoursePut(CourseBase):
    pass

class CoursePatch(BaseModel):
    duration_hours: int = Field(ge=0)