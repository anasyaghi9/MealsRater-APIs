# MealsRater API

A REST API built with **Django** and **Django REST Framework** that lets users register, browse meals, and rate them (1–5 stars). Each meal shows its live average rating and total number of ratings.

## Tech Stack

- **Python / Django** — web framework
- **Django REST Framework (DRF)** — REST API layer
- **DRF Token Authentication** — auth via `Authorization: Token <key>`
- **SQLite** — default local database

## Project Structure

```
mealrater/
├── api/                  # Main app: models, serializers, views, routes
│   ├── models.py         # Meal, Rating
│   ├── serializers.py    # UserSerializer, MealSerializer, RatingSerializer
│   ├── views.py          # UserViewSet, MealViewSet, RatingViewSet
│   └── urls.py           # DRF router registration
├── mealrater/            # Project settings
│   ├── settings.py
│   ├── urls.py           # Root URL config
│   └── wsgi.py / asgi.py
├── manage.py
└── db.sqlite3
```

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/anasyaghi9/MealsRater-APIs.git
cd MealsRater-APIs/mealrater

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux

# 3. Install dependencies
pip install django djangorestframework

# 4. Apply migrations
python manage.py migrate

# 5. Run the server
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## Authentication

The API uses **DRF Token Authentication**. Register a user, then request a token, then send it on every subsequent request.

```
Authorization: Token <your-token-here>
```

`Meal` and `Rating` endpoints require a valid token. `User` endpoints (register, retrieve, update, delete) don't require one.

---

## API Endpoints

### Users — `/api/user/`

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/api/user/` | None | Register a new user. Returns an auth token. |
| `GET` | `/api/user/` | None | Disabled — returns 400. |
| `GET` | `/api/user/{id}/` | None | Retrieve a user (`id`, `username`). |
| `PUT` | `/api/user/{id}/` | None | Full update of a user. |
| `PATCH` | `/api/user/{id}/` | None | Partial update of a user. |
| `DELETE` | `/api/user/{id}/` | None | Delete a user. |

**Register — request:**
```json
POST /api/user/
{ "username": "alice", "password": "testpass123" }
```

**Response — `201 Created`:**
```json
{ "token": "869b25a5ea128d7c8626abead0570f30d46f87e6" }
```

### Token — `/tokenrequest/`

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/tokenrequest/` | None | Exchange username/password for an auth token. |

**Request:**
```json
{ "username": "alice", "password": "testpass123" }
```

**Response — `200 OK`:**
```json
{ "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" }
```

### Meals — `/api/meal/`

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/api/meal/` | Token | List all meals, with rating count & average. |
| `POST` | `/api/meal/` | Token | Create a meal. |
| `GET` | `/api/meal/{id}/` | Token | Retrieve one meal. |
| `PUT` | `/api/meal/{id}/` | Token | Full update of a meal. |
| `PATCH` | `/api/meal/{id}/` | Token | Partial update of a meal. |
| `DELETE` | `/api/meal/{id}/` | Token | Delete a meal. |
| `POST` | `/api/meal/{id}/rate_meal/` | Token | Create or update **the caller's own** rating for this meal. |

**Create a meal — request:**
```json
POST /api/meal/
{ "title": "Pizza", "description": "Cheesy delight" }
```

**Response — `201 Created`:**
```json
{ "id": 1, "title": "Pizza", "description": "Cheesy delight", "no_of_ratings": 0, "avg_rating": 0 }
```

**Rate a meal — request:**
```json
POST /api/meal/1/rate_meal/
{ "stars": 4 }
```

- First time rating this meal → `201 Created`, `{"message": "Meal Rate Created", "result": {...}}`
- Rating it again → `200 OK`, `{"message": "Meal Rate Updated", "result": {...}}` (updates in place, doesn't duplicate)
- `stars` missing → `400`, `{"message": "stars not provided"}`
- `stars` outside 1–5 or not a number → `400`, `{"message": "Invalid data", "errors": {...}}`
- Meal not found → `404`, `{"message": "Meal not found"}`

### Ratings — `/api/rating/`

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/api/rating/` | Token | List all ratings. |
| `GET` | `/api/rating/{id}/` | Token | Retrieve one rating. |
| `POST` | `/api/rating/` | Token | Disabled — use `rate_meal` instead. Returns 405. |
| `PUT` / `PATCH` | `/api/rating/{id}/` | Token | Disabled — use `rate_meal` instead. Returns 405. |
| `DELETE` | `/api/rating/{id}/` | Token | Delete a rating by id. |

---

## Data Models

**Meal**
| Field | Type | Notes |
|---|---|---|
| `title` | string | max 32 chars |
| `description` | string | max 360 chars |
| `no_of_ratings` | computed | count of related ratings |
| `avg_rating` | computed | average of related ratings' stars |

**Rating**
| Field | Type | Notes |
|---|---|---|
| `meal` | FK → Meal | |
| `user` | FK → User | |
| `stars` | int | 1–5 (validated) |

A `(user, meal)` pair is unique — one rating per user per meal.
