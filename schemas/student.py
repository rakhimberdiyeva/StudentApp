from pydantic import BaseModel, Field


class StudentBase(BaseModel):
    fullname: str
    age: int = Field(ge=1)
    is_active: bool

class StudentCreate(StudentBase):
    pass

class StudentPut(StudentBase):
    pass

class StudentPatch(BaseModel):
    is_active: bool