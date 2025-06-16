from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas, models
from app.auth import require_roles

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

@router.get("/", response_model=List[schemas.Session])
async def read_sessions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_sessions(db, skip=skip, limit=limit)

@router.get("/{session_id}", response_model=schemas.Session)
async def read_session(session_id: int, db: Session = Depends(get_db)):
    session = crud.get_session(db, session_id=session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/", response_model=schemas.Session)
async def create_session(
    session: schemas.SessionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles(["admin", "cashier"]))
):
    # Проверяем существование фильма и зала
    movie = crud.get_movie(db, session.movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    hall = crud.get_hall(db, session.hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    return crud.create_session(db=db, session=session)

@router.put("/{session_id}", response_model=schemas.Session)
async def update_session(
    session_id: int,
    session_update: schemas.SessionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles(["admin", "cashier"]))
):
    session = crud.update_session(db, session_id, session_update)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/{session_id}")
async def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles(["admin", "cashier"]))
):
    session = crud.delete_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}