from pydantic import BaseModel, Field

class EnrollmentBase(BaseModel):
    student_id: int = Field(ge=1)
    course_id: int = Field(ge=1)

class EnrollmentCreate(EnrollmentBase):
    pass