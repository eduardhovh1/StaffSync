from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TrabajadorBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(max_length=100)
    departamento_id: int | None = Field(default=None, gt=0)


class TrabajadorCreate(TrabajadorBase):
    pass


class TrabajadorUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = Field(default=None, max_length=100)
    departamento_id: int | None = Field(default=None, gt=0)


class TrabajadorResponse(TrabajadorBase):
    id: int
    fecha_contratacion: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
