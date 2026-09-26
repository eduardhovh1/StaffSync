from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class Departamento(Base):
    __tablename__ = "departamentos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

    trabajadores: Mapped[list["Trabajador"]] = relationship(
        "Trabajador", back_populates="departamento", passive_deletes=True
    )
