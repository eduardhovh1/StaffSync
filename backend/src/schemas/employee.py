from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(max_length=100)
    department_id: int | None = Field(default=None, gt=0)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = Field(default=None, max_length=100)
    department_id: int | None = Field(default=None, gt=0)


class EmployeeResponse(EmployeeBase):
    id: int
    hire_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
