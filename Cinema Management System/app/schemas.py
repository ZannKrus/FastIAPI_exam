from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    VIEWER = "viewer"
    CASHIER = "cashier"
    ADMIN = "admin"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.VIEWER

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class MovieBase(BaseModel):
    title: str
    genre: str
    duration: int
    rating: float
    description: Optional[str] = None
    
    @validator('duration')
    def validate_duration(cls, v):
        if v <= 0:
            raise ValueError('Duration must be positive')
        return v
    
    @validator('rating')
    def validate_rating(cls, v):
        if not 0 <= v <= 10:
            raise ValueError('Rating must be between 0 and 10')
        return v

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    duration: Optional[int] = None
    rating: Optional[float] = None
    description: Optional[str] = None

class Movie(MovieBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class HallBase(BaseModel):
    name: str
    capacity: int
    
    @validator('capacity')
    def validate_capacity(cls, v):
        if v <= 0:
            raise ValueError('Capacity must be positive')
        return v

class HallCreate(HallBase):
    pass

class Hall(HallBase):
    id: int
    
    class Config:
        from_attributes = True

class SessionBase(BaseModel):
    movie_id: int
    hall_id: int
    start_time: datetime
    price: float
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    movie_id: Optional[int] = None
    hall_id: Optional[int] = None
    start_time: Optional[datetime] = None
    price: Optional[float] = None

class Session(SessionBase):
    id: int
    created_at: datetime
    movie: Movie
    hall: Hall
    
    class Config:
        from_attributes = True

class TicketBase(BaseModel):
    session_id: int
    seat_number: str

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int
    user_id: int
    purchased_at: datetime
    session: Session
    
    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    movie_id: int
    rating: int
    comment: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if not 1 <= v <= 10:
            raise ValueError('Rating must be between 1 and 10')
        return v

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    user_id: int
    created_at: datetime
    user: User
    
    class Config:
        from_attributes = True