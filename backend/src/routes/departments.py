from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.department import Department
from src.schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)

router = APIRouter(prefix="/api/departments", tags=["departments"])


@router.get("/", response_model=list[DepartmentResponse])
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(department_id: int, db: Session = Depends(get_db)):
    obj = db.get(Department, department_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Department not found")
    return obj


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db)):
    obj = Department(name=payload.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int, payload: DepartmentUpdate, db: Session = Depends(get_db)
):
    obj = db.get(Department, department_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Department not found")
    if payload.name is not None:
        obj.name = payload.name
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    obj = db.get(Department, department_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(obj)
    db.commit()
    return None
