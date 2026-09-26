from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class Trabajador(Base):
    __tablename__ = "trabajadores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    departamento_id: Mapped[int | None] = mapped_column(
        ForeignKey("departamentos.id", ondelete="SET NULL"), nullable=True
    )
    fecha_contratacion: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp(), nullable=True
    )

    departamento: Mapped["Departamento | None"] = relationship(
        "Departamento", back_populates="trabajadores"
    )
