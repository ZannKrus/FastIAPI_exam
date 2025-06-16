from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas, models
from app.auth import require_role

router = APIRouter(prefix="/api/halls", tags=["halls"])

@router.get("/", response_model=List[schemas.Hall])
async def read_halls(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_halls(db, skip=skip, limit=limit)

@router.get("/{hall_id}", response_model=schemas.Hall)
async def read_hall(hall_id: int, db: Session = Depends(get_db)):
    hall = crud.get_hall(db, hall_id=hall_id)
    if hall is None:
        raise HTTPException(status_code=404, detail="Hall not found")
    return hall

@router.post("/", response_model=schemas.Hall)
async def create_hall(
    hall: schemas.HallCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin"))
):
    return crud.create_hall(db=db, hall=hall)