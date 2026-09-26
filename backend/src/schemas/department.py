from pydantic import BaseModel, ConfigDict, Field


class DepartmentBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)


class DepartmentResponse(DepartmentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
