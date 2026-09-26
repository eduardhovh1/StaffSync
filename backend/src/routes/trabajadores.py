from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.departamento import Departamento
from src.models.trabajador import Trabajador
from src.schemas.trabajador import (
    TrabajadorCreate,
    TrabajadorResponse,
    TrabajadorUpdate,
)

router = APIRouter(prefix="/api/trabajadores", tags=["trabajadores"])


def _validar_departamento(db: Session, departamento_id: int | None) -> None:
    if departamento_id is None:
        return
    if db.get(Departamento, departamento_id) is None:
        raise HTTPException(status_code=400, detail="departamento_id no existe")


@router.get("/", response_model=list[TrabajadorResponse])
def listar_trabajadores(db: Session = Depends(get_db)):
    return db.query(Trabajador).all()


@router.get("/{trabajador_id}", response_model=TrabajadorResponse)
def obtener_trabajador(trabajador_id: int, db: Session = Depends(get_db)):
    obj = db.get(Trabajador, trabajador_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return obj


@router.post("/", response_model=TrabajadorResponse, status_code=status.HTTP_201_CREATED)
def crear_trabajador(payload: TrabajadorCreate, db: Session = Depends(get_db)):
    _validar_departamento(db, payload.departamento_id)
    obj = Trabajador(
        nombre=payload.nombre,
        email=payload.email,
        departamento_id=payload.departamento_id,
    )
    db.add(obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email ya registrado")
    db.refresh(obj)
    return obj


@router.put("/{trabajador_id}", response_model=TrabajadorResponse)
def actualizar_trabajador(
    trabajador_id: int, payload: TrabajadorUpdate, db: Session = Depends(get_db)
):
    obj = db.get(Trabajador, trabajador_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    data = payload.model_dump(exclude_unset=True)
    if "departamento_id" in data:
        _validar_departamento(db, data["departamento_id"])
    for field, value in data.items():
        setattr(obj, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email ya registrado")
    db.refresh(obj)
    return obj


@router.delete("/{trabajador_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_trabajador(trabajador_id: int, db: Session = Depends(get_db)):
    obj = db.get(Trabajador, trabajador_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    db.delete(obj)
    db.commit()
    return None
