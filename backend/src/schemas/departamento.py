from pydantic import BaseModel, ConfigDict, Field


class DepartamentoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)


class DepartamentoCreate(DepartamentoBase):
    pass


class DepartamentoUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)


class DepartamentoResponse(DepartamentoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
