from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.department import Department
from src.models.employee import Employee
from src.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)

router = APIRouter(prefix="/api/employees", tags=["employees"])


def _validate_department(db: Session, department_id: int | None) -> None:
    if department_id is None:
        return
    if db.get(Department, department_id) is None:
        raise HTTPException(status_code=400, detail="department_id does not exist")


@router.get("/", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    obj = db.get(Employee, employee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    return obj


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    _validate_department(db, payload.department_id)
    obj = Employee(
        name=payload.name,
        email=payload.email,
        department_id=payload.department_id,
    )
    db.add(obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    db.refresh(obj)
    return obj


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int, payload: EmployeeUpdate, db: Session = Depends(get_db)
):
    obj = db.get(Employee, employee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    data = payload.model_dump(exclude_unset=True)
    if "department_id" in data:
        _validate_department(db, data["department_id"])
    for field, value in data.items():
        setattr(obj, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    db.refresh(obj)
    return obj


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    obj = db.get(Employee, employee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(obj)
    db.commit()
    return None
