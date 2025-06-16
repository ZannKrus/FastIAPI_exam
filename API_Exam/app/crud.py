from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app import models, schemas
from app.auth import get_password_hash
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created: {user.username}")
    return db_user

# Movie CRUD
def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def get_movies(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    genre: Optional[str] = None,
    min_rating: Optional[float] = None
):
    query = db.query(models.Movie)
    
    if genre:
        query = query.filter(models.Movie.genre.ilike(f"%{genre}%"))
    if min_rating:
        query = query.filter(models.Movie.rating >= min_rating)
    
    return query.offset(skip).limit(limit).all()

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    logger.info(f"Movie created: {movie.title}")
    return db_movie

def update_movie(db: Session, movie_id: int, movie_update: schemas.MovieUpdate):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie:
        update_data = movie_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_movie, field, value)
        db.commit()
        db.refresh(db_movie)
        logger.info(f"Movie updated: {db_movie.title}")
    return db_movie

def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie:
        db.delete(db_movie)
        db.commit()
        logger.info(f"Movie deleted: {db_movie.title}")
    return db_movie

# Hall CRUD
def get_hall(db: Session, hall_id: int):
    return db.query(models.Hall).filter(models.Hall.id == hall_id).first()

def get_halls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Hall).offset(skip).limit(limit).all()

def create_hall(db: Session, hall: schemas.HallCreate):
    db_hall = models.Hall(**hall.dict())
    db.add(db_hall)
    db.commit()
    db.refresh(db_hall)
    logger.info(f"Hall created: {hall.name}")
    return db_hall

# Session CRUD
def get_session(db: Session, session_id: int):
    return db.query(models.Session).filter(models.Session.id == session_id).first()

def get_sessions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Session).offset(skip).limit(limit).all()

def create_session(db: Session, session: schemas.SessionCreate):
    db_session = models.Session(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    logger.info(f"Session created: {session.movie_id}")
    return db_session

def update_session(db: Session, session_id: int, session_update: schemas.SessionUpdate):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if db_session:
        update_data = session_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_session, field, value)
        db.commit()
        db.refresh(db_session)
        logger.info(f"Session updated: {session_id}")
    return db_session

def delete_session(db: Session, session_id: int):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if db_session:
        db.delete(db_session)
        db.commit()
        logger.info(f"Session deleted: {session_id}")
    return db_session

# Ticket CRUD
def get_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

def get_user_tickets(db: Session, user_id: int):
    return db.query(models.Ticket).filter(models.Ticket.user_id == user_id).all()

def create_ticket(db: Session, ticket: schemas.TicketCreate, user_id: int):
    # Проверка на занятость места
    existing_ticket = db.query(models.Ticket).filter(
        and_(
            models.Ticket.session_id == ticket.session_id,
            models.Ticket.seat_number == ticket.seat_number
        )
    ).first()
    
    if existing_ticket:
        raise ValueError("Seat already taken")
    
    db_ticket = models.Ticket(**ticket.dict(), user_id=user_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    logger.info(f"Ticket created: user {user_id}, session {ticket.session_id}")
    return db_ticket

# Review CRUD
def get_movie_reviews(db: Session, movie_id: int):
    return db.query(models.Review).filter(models.Review.movie_id == movie_id).all()

def create_review(db: Session, review: schemas.ReviewCreate, user_id: int):
    # Проверка, что пользователь еще не оставлял отзыв на этот фильм
    existing_review = db.query(models.Review).filter(
        and_(
            models.Review.movie_id == review.movie_id,
            models.Review.user_id == user_id
        )
    ).first()
    
    if existing_review:
        raise ValueError("User already reviewed this movie")
    
    db_review = models.Review(**review.dict(), user_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    logger.info(f"Review created: user {user_id}, movie {review.movie_id}")
    return db_review