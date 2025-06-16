from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas, models
from app.auth import get_current_user

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

@router.get("/movie/{movie_id}", response_model=List[schemas.Review])
async def read_movie_reviews(movie_id: int, db: Session = Depends(get_db)):
    movie = crud.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return crud.get_movie_reviews(db, movie_id)

@router.post("/", response_model=schemas.Review)
async def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Проверяем существование фильма
    movie = crud.get_movie(db, review.movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    try:
        return crud.create_review(db=db, review=review, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))