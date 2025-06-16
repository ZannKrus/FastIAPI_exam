from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas, models
from app.auth import get_current_user, require_roles

router = APIRouter(prefix="/api/tickets", tags=["tickets"])

@router.get("/my", response_model=List[schemas.Ticket])
async def read_my_tickets(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_tickets(db, current_user.id)

@router.get("/{ticket_id}", response_model=schemas.Ticket)
async def read_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Пользователи могут видеть только свои билеты, кассиры и админы - все
    if current_user.role == "viewer" and ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return ticket

@router.post("/", response_model=schemas.Ticket)
async def buy_ticket(
    ticket: schemas.TicketCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Проверяем существование сеанса
    session = crud.get_session(db, ticket.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        return crud.create_ticket(db=db, ticket=ticket, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))