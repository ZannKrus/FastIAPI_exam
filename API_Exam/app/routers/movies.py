from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas, models
from app.auth import get_current_user, require_role

router = APIRouter(prefix="/api/movies", tags=["movies"])

@router.get("/", response_model=List[schemas.Movie])
async def read_movies(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    genre: Optional[str] = None,
    minRating: Optional[float] = Query(None, alias="minRating", ge=0, le=10),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    movies = crud.get_movies(
        db, 
        skip=skip, 
        limit=limit,
        genre=genre,
        min_rating=minRating
    )
    return movies

@router.get("/{movie_id}", response_model=schemas.Movie)
async def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = crud.get_movie(db, movie_id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/", response_model=schemas.Movie)
async def create_movie(
    movie: schemas.MovieCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin"))
):
    return crud.create_movie(db=db, movie=movie)

@router.put("/{movie_id}", response_model=schemas.Movie)
async def update_movie(
    movie_id: int,
    movie_update: schemas.MovieUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin"))
):
    movie = crud.update_movie(db, movie_id, movie_update)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.delete("/{movie_id}")
async def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin"))
):
    movie = crud.delete_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}