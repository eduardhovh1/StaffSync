from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.departamento import Departamento
from src.schemas.departamento import (
    DepartamentoCreate,
    DepartamentoResponse,
    DepartamentoUpdate,
)

router = APIRouter(prefix="/api/departamentos", tags=["departamentos"])


@router.get("/", response_model=list[DepartamentoResponse])
def listar_departamentos(db: Session = Depends(get_db)):
    return db.query(Departamento).all()


@router.get("/{departamento_id}", response_model=DepartamentoResponse)
def obtener_departamento(departamento_id: int, db: Session = Depends(get_db)):
    obj = db.get(Departamento, departamento_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    return obj


@router.post("/", response_model=DepartamentoResponse, status_code=status.HTTP_201_CREATED)
def crear_departamento(payload: DepartamentoCreate, db: Session = Depends(get_db)):
    obj = Departamento(nombre=payload.nombre)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{departamento_id}", response_model=DepartamentoResponse)
def actualizar_departamento(
    departamento_id: int, payload: DepartamentoUpdate, db: Session = Depends(get_db)
):
    obj = db.get(Departamento, departamento_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    if payload.nombre is not None:
        obj.nombre = payload.nombre
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{departamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_departamento(departamento_id: int, db: Session = Depends(get_db)):
    obj = db.get(Departamento, departamento_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    db.delete(obj)
    db.commit()
    return None
