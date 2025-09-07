# Video Project

Проект Django с PostgreSQL, Gunicorn и Nginx в Docker.


## 🛠️ Используемые технологии

- Django / Django REST Framework
- PostgreSQL
- Nginx
- Docker
- Docker-compose
- uv

## Клонирование проекта

```bash
git clone git@github.com:malabr1sta/video_project.git
cd video_project
cp env_template .env
uv run collectstatic
```

## 🐳 Запуск через Docker Compose

```bash
docker-compose up --build
docker exec -it video_web python manage.py migrate
docker exec -it video_web python manage.py createsuperuser
```

## 🌐 Доступ к сервису

- **Админка:** [http://127.0.0.1/admin/](http://127.0.0.1/admin/)
- **Документация API:** [http://127.0.0.1/api/docs/](http://127.0.0.1/docs/)
