from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, crud, schemas
from app.auth import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    models.Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    try:
        # Создаем пользователей
        users_data = [
            {
                "username": "admin",
                "email": "admin@cinema.com",
                "password": "admin123",
                "role": "admin"
            },
            {
                "username": "cashier",
                "email": "cashier@cinema.com", 
                "password": "cashier123",
                "role": "cashier"
            },
            {
                "username": "viewer1",
                "email": "viewer1@cinema.com",
                "password": "viewer123", 
                "role": "viewer"
            },
            {
                "username": "viewer2",
                "email": "viewer2@cinema.com",
                "password": "viewer123",
                "role": "viewer"
            }
        ]
        
        for user_data in users_data:
            existing_user = db.query(models.User).filter(
                models.User.username == user_data["username"]
            ).first()
            if not existing_user:
                user_schema = schemas.UserCreate(**user_data)
                crud.create_user(db, user_schema)
                logger.info(f"Created user: {user_data['username']}")
        
        # Создаем залы
        halls_data = [
            {"name": "Зал 1", "capacity": 100},
            {"name": "Зал 2", "capacity": 150},
            {"name": "Зал 3", "capacity": 80},
            {"name": "IMAX Зал", "capacity": 200}
        ]
        
        for hall_data in halls_data:
            existing_hall = db.query(models.Hall).filter(
                models.Hall.name == hall_data["name"]
            ).first()
            if not existing_hall:
                hall_schema = schemas.HallCreate(**hall_data)
                crud.create_hall(db, hall_schema)
                logger.info(f"Created hall: {hall_data['name']}")
        
        # Создаем фильмы
        movies_data = [
            {
                "title": "Мстители: Финал",
                "genre": "action",
                "duration": 181,
                "rating": 8.4,
                "description": "Эпический финал саги о Мстителях"
            },
            {
                "title": "Джокер",
                "genre": "drama", 
                "duration": 122,
                "rating": 8.5,
                "description": "История происхождения самого известного злодея"
            },
            {
                "title": "Человек-паук: Нет пути домой",
                "genre": "action",
                "duration": 148,
                "rating": 8.2,
                "description": "Мультивселенная Человека-паука"
            },
            {
                "title": "Дюна",
                "genre": "sci-fi",
                "duration": 155,
                "rating": 8.0,
                "description": "Эпическая научная фантастика Дени Вильнёва"
            },
            {
                "title": "Не время умирать",
                "genre": "action",
                "duration": 163,
                "rating": 7.3,
                "description": "Последний фильм о Джеймсе Бонде с Дэниелом Крейгом"
            },
            {
                "title": "Парасит",
                "genre": "thriller",
                "duration": 132,
                "rating": 8.6,
                "description": "Корейский триллер, получивший Оскар"
            },
            {
                "title": "Форма воды",
                "genre": "fantasy",
                "duration": 123,
                "rating": 7.3,
                "description": "Романтическая фантастика Гильермо дель Торо"
            },
            {
                "title": "Интерстеллар",
                "genre": "sci-fi",
                "duration": 169,
                "rating": 8.6,
                "description": "Космическая одиссея Кристофера Нолана"
            },
            {
                "title": "Однажды в Голливуде",
                "genre": "comedy",
                "duration": 161,
                "rating": 7.6,
                "description": "Комедийная драма Квентина Тарантино"
            },
            {
                "title": "Зеленая книга",
                "genre": "drama",
                "duration": 130,
                "rating": 8.2,
                "description": "Драма о дружбе и преодолении предрассудков"
            }
        ]
        
        for movie_data in movies_data:
            existing_movie = db.query(models.Movie).filter(
                models.Movie.title == movie_data["title"]
            ).first()
            if not existing_movie:
                movie_schema = schemas.MovieCreate(**movie_data)
                crud.create_movie(db, movie_schema)
                logger.info(f"Created movie: {movie_data['title']}")
        
        # Создаем сеансы
        from datetime import datetime, timedelta
        
        sessions_data = [
            {
                "movie_id": 1,
                "hall_id": 1,
                "start_time": datetime.now() + timedelta(hours=2),
                "price": 350.0
            },
            {
                "movie_id": 1,
                "hall_id": 1,
                "start_time": datetime.now() + timedelta(hours=6),
                "price": 400.0
            },
            {
                "movie_id": 2,
                "hall_id": 2,
                "start_time": datetime.now() + timedelta(hours=3),
                "price": 300.0
            },
            {
                "movie_id": 3,
                "hall_id": 4,
                "start_time": datetime.now() + timedelta(hours=4),
                "price": 500.0
            },
            {
                "movie_id": 4,
                "hall_id": 3,
                "start_time": datetime.now() + timedelta(hours=5),
                "price": 450.0
            }
        ]
        
        for session_data in sessions_data:
            session_schema = schemas.SessionCreate(**session_data)
            crud.create_session(db, session_schema)
            logger.info(f"Created session for movie {session_data['movie_id']}")
        
        logger.info("Database seeded successfully!")
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    seed_database()