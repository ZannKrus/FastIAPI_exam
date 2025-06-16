# Cinema Management System API

## Описание проекта

Cinema Management System - это REST API для управления кинотеатром, реализованное на FastAPI. Система включает в себя управление фильмами, сеансами, билетами и отзывами с системой аутентификации и ролями пользователей.

**Вариант 4: Кинотеатр (афиша и билеты)**

### Основной функционал:
- Управление фильмами (CRUD операции)
- Управление сеансами кинотеатра
- Система продажи билетов
- Система отзывов к фильмам
- Аутентификация и авторизация пользователей
- Роли пользователей (Зритель, Кассир, Администратор)
- Пагинация и фильтрация
- Валидация входных данных
- Логирование всех операций

## Используемые технологии

- **Python** 3.12.* - **Важно!** 3.13 некорректно устанавливает компоненты. 
- **FastAPI** 0.104.1 - веб-фреймворк
- **SQLAlchemy** 2.0.23 - ORM для работы с базой данных
- **SQLite** - легкая база данных для учебного проекта
- **Pydantic** 2.5.0 - валидация данных
- **python-jose** 3.3.0 - JWT токены
- **passlib** 1.7.4 - хеширование паролей
- **uvicorn** 0.24.0 - ASGI сервер

## Инструкция по запуску

### 1. Клонирование репозитория
```bash
git clone https://github.com/ZannKrus/FastIAPI_exam.git
cd FastIAPI_exam
```

### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Инициализация базы данных и seed данных
```bash
python seed.py
```

### 5. Запуск приложения
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

## API Документация

### Методология API
- **REST API** - следует принципам REST архитектуры
- **JSON** - формат передачи данных
- **JWT Bearer Token** - аутентификация

### Документация эндпоинтов
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Основные эндпоинты

#### Аутентификация
- `POST /auth/login` - вход в систему
- `POST /auth/register` - регистрация пользователя

#### Фильмы
- `GET /api/movies` - получение списка фильмов (с пагинацией и фильтрацией)
- `GET /api/movies/{id}` - получение фильма по ID
- `POST /api/movies` - создание фильма (только админ)
- `PUT /api/movies/{id}` - обновление фильма (только админ)
- `DELETE /api/movies/{id}` - удаление фильма (только админ)

#### Сеансы
- `GET /api/sessions` - получение списка сеансов
- `GET /api/sessions/{id}` - получение сеанса по ID
- `POST /api/sessions` - создание сеанса (админ/кассир)
- `PUT /api/sessions/{id}` - обновление сеанса (админ/кассир)
- `DELETE /api/sessions/{id}` - удаление сеанса (админ/кассир)

#### Билеты
- `GET /api/tickets/my` - получение билетов текущего пользователя
- `GET /api/tickets/{id}` - получение билета по ID
- `POST /api/tickets` - покупка билета

#### Отзывы
- `GET /api/reviews/movie/{movie_id}` - получение отзывов к фильму
- `POST /api/reviews` - создание отзыва

#### Залы
- `GET /api/halls` - получение списка залов
- `GET /api/halls/{id}` - получение зала по ID
- `POST /api/halls` - создание зала (только админ)

### Ключевой эндпоинт с фильтрацией
```
GET /api/movies?page=1&limit=10&genre=comedy&minRating=7
```

**Параметры:**
- `page` (int, >=1) - номер страницы
- `limit` (int, 1-100) - количество элементов на странице
- `genre` (string) - фильтр по жанру (частичное совпадение)
- `minRating` (float, 0-10) - минимальный рейтинг

## Валидация

### Валидация фильмов
- **title**: обязательное поле, строка
- **genre**: обязательное поле, строка
- **duration**: положительное число (минуты)
- **rating**: число от 0 до 10

### Валидация сеансов
- **movie_id**: существующий ID фильма
- **hall_id**: существующий ID зала
- **start_time**: корректная дата и время
- **price**: положительное число

### Валидация билетов
- **session_id**: существующий ID сеанса
- **seat_number**: уникальность в рамках сеанса

### Валидация отзывов
- **movie_id**: существующий ID фильма
- **rating**: число от 1 до 10
- **user_id**: один отзыв на фильм от пользователя

## Роли пользователей

### Зритель (viewer)
- Просмотр фильмов и сеансов
- Покупка билетов
- Создание отзывов
- Просмотр своих билетов

### Кассир (cashier)
- Все права зрителя
- Управление сеансами (создание, изменение, удаление)
- Просмотр всех билетов

### Администратор (admin)
- Все права кассира
- Управление фильмами (создание, изменение, удаление)
- Управление залами
- Полный доступ к системе

## Тестовые пользователи

После выполнения seed'а будут созданы следующие пользователи:

| Роль | Username | Password | Email |
|------|----------|----------|-------|
| Администратор | admin | admin123 | admin@cinema.com |
| Кассир | cashier | cashier123 | cashier@cinema.com |
| Зритель | viewer1 | viewer123 | viewer1@cinema.com |
| Зритель | viewer2 | viewer123 | viewer2@cinema.com |

## База данных

База данных SQLite спроектирована в соответствии с 3-й нормальной формой:

### Основные таблицы:
- **users** - пользователи системы
- **movies** - фильмы
- **halls** - залы кинотеатра
- **sessions** - сеансы
- **tickets** - билеты
- **reviews** - отзывы к фильмам

### Связи:
- User ↔ Ticket (один ко многим)
- User ↔ Review (один ко многим)
- Movie ↔ Session (один ко многим)
- Movie ↔ Review (один ко многим)
- Hall ↔ Session (один ко многим)
- Session ↔ Ticket (один ко многим)

### Файл базы данных
База данных хранится в файле `cinema.db` в корне проекта. Для просмотра можно использовать любой SQLite браузер.

## Логирование

Система ведет подробные логи всех операций:
- Входящие HTTP запросы
- Время выполнения запросов
- CRUD операции с сущностями
- Ошибки валидации
- Ошибки базы данных

Логи выводятся в консоль в формате:
```
2024-01-01 12:00:00 - app.main - INFO - Request: GET /api/movies
```

## Примеры использования

### 1. Аутентификация
```bash
# Вход в систему
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### 2. Получение фильмов с фильтрацией
```bash
curl "http://localhost:8000/api/movies?page=1&limit=5&genre=action&minRating=8"
```

### 3. Создание фильма (требует токен админа)
```bash
curl -X POST "http://localhost:8000/api/movies" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Новый фильм",
    "genre": "drama",
    "duration": 120,
    "rating": 8.5,
    "description": "Описание фильма"
  }'
```

### 4. Покупка билета
```bash
curl -X POST "http://localhost:8000/api/tickets" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1,
    "seat_number": "A1"
  }'
```

## Структура проекта
```
cinema-management-system/
├── app/
│   ├── main.py           # Основное приложение FastAPI
│   ├── database.py       # Настройка базы данных
│   ├── models.py         # SQLAlchemy модели
│   ├── schemas.py        # Pydantic схемы
│   ├── auth.py          # Аутентификация и авторизация
│   ├── crud.py          # CRUD операции
│   └── routers/         # API роутеры
│       ├── auth.py
│       ├── movies.py
│       ├── sessions.py
│       ├── tickets.py
│       ├── reviews.py
│       └── halls.py
├── requirements.txt      # Зависимости Python
├── seed.py               # Наполнение базы тестовыми данными
├── .env.example        # Пример переменных окружения
├── cinema.db           # SQLite база данных (создается автоматически)
└── README.md           # Документация
```

## Контакты

**Разработчик**: Юсупов Дамир

**Email**: damiryusupov2504@gmail.com

**Telegram**: @ZannKrus

## Лицензия

MIT License