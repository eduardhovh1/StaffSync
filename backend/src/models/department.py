from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    employees: Mapped[list["Employee"]] = relationship(
        "Employee", back_populates="department", passive_deletes=True
    )
