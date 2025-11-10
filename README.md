# DRF
This project is designed to display courses and lessons that the user can create.
## Materials
Contains the necessary classes, accesses, validators, and tests for correct operation.
## User
Similarly, it contains classes for interacting with materials, and there is also the option to pay for the course.
## Run 
1. Clone repository
git clone https://github.com/yourusername/yourproject.git
cd yourproject
2. Create .env file (templates on .env.templates)
3. Collect and run container
docker-compose up --build
4. Tests
docker-compose logs web
docker exec -it postgres_db psql -U django_user -d django_rest
docker-compose logs db
docker exec -it redis redis-cli ping
docker-compose logs redis
docker-compose logs celery
docker-compose logs celery-beat