# Video Project

Django project with PostgreSQL, Gunicorn, and Nginx in Docker.  
REST API for managing videos, likes, and statistics.

## 📌 Project Description

This project allows users to:

- Upload videos  
- Like/unlike videos  
- View statistics of likes per user  

The API is built using **Django REST Framework**, secured with **JWT authentication**.  
Staff users can access endpoints for statistics and video IDs.

## 🛠️ Technologies Used

- Django / Django REST Framework  
- PostgreSQL  
- Nginx  
- Docker & Docker Compose  
- uv  

## 💻 Installation & Setup

### Clone the repository

```bash
git clone git@github.com:malabr1sta/video_project.git
cd video_project
cp env_template .env
uv run collectstatic
```

### Run with Docker Compose

```bash
docker-compose up --build
docker exec -it video_web python manage.py migrate
docker exec -it video_web python manage.py createsuperuser
```

### Access

- **Admin panel:** [http://127.0.0.1/admin/](http://127.0.0.1/admin/)  
- **Swagger API docs:** [http://127.0.0.1/docs/](http://127.0.0.1/docs/)

## 🔑 Authentication (JWT)

### Obtain token

```http
POST /v1/accounts/auth/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

Response:

```json
{
  "refresh": "refresh_token",
  "access": "access_token"
}
```

### Refresh token

```http
POST /v1/accounts/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "refresh_token"
}
```

### Verify token

```http
POST /v1/accounts/auth/token/verify/
Content-Type: application/json

{
  "token": "access_token"
}
```

### Register new user

```http
POST /v1/accounts/auth/register/
Content-Type: application/json

{
  "username": "new_user",
  "password": "new_password"
}
```

Response:

```json
{
  "id": 1,
  "username": "new_user"
}
```

## 🎬 Videos API

### List all videos

```http
GET /v1/videos/
Authorization: Bearer <access_token>
```

Response:

```json
[
  {
    "id": 1,
    "owner": "username",
    "name": "Video Name",
    "total_likes": 10,
    "created_at": "2025-09-07T14:00:00Z",
    "files": [
      {"id": 1, "file": "url_to_file", "quality": "HD"}
    ]
  }
]
```

### Retrieve video details

```http
GET /v1/videos/<video_id>/
Authorization: Bearer <access_token>
```

Response:

```json
{
  "id": 1,
  "owner": "username",
  "name": "Video Name",
  "total_likes": 10,
  "created_at": "2025-09-07T14:00:00Z",
  "files": [
    {"id": 1, "file": "url_to_file", "quality": "HD"}
  ]
}
```

### Video IDs (Staff Only)

```http
GET /v1/videos/ids/
Authorization: Bearer <staff_access_token>
```

Response:

```json
[
  {"id": 1, "username": "username"},
  {"id": 2, "username": "another_user"}
]
```

## ❤️ Likes API

### Like a video

```http
POST /v1/videos/<video_id>/likes/
Authorization: Bearer <access_token>
```

Response (created):

```json
{
  "obj": 1,
  "created": true
}
```

Response (already liked):

```json
{
  "obj": 1,
  "created": false
}
```

### Unlike a video

```http
DELETE /v1/videos/<video_id>/likes/
Authorization: Bearer <access_token>
```

Response (deleted):

```
HTTP 204 No Content
```

Response (not deleted):

```
HTTP 400 Bad Request
```

## 📊 Statistics API (Staff Only)

### Group by Owner

```http
GET /v1/videos/statistics-group-by/
Authorization: Bearer <staff_access_token>
```

Response:

```json
[
  {"username": "user1", "likes_sum": 10},
  {"username": "user2", "likes_sum": 5}
]
```

### Subquery Statistics

```http
GET /v1/videos/statistics-subquery/
Authorization: Bearer <staff_access_token>
```

Response:

```json
[
  {"username": "user1", "likes_sum": 10},
  {"username": "user2", "likes_sum": 5}
]
```

## ⚙️ Notes

- Only staff users can access video IDs and statistics endpoints.  
- Authenticated users can see their own unpublished videos in addition to published ones.  
- JWT token required for all protected endpoints.  
- Swagger documentation available at `/docs/` for interactive API testing.  
