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
5. Установка Docker и Docker Compose
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker --version
docker-compose --version
6. Настройка SSH для деплоя через GitHub Actions
ssh-keygen -t rsa -b 4096 -C "github-actions-deploy" -f gh-actions-deploy-key
7. Добавить публичный ключ на сервер:
ssh user@your_server
mkdir -p ~/.ssh
echo "СОДЕРЖИМОЕ ФАЙЛА gh-actions-deploy-key.pub" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
8. Проверить подключение:
ssh -i gh-actions-deploy-key user@your_server
9. Разворачивание проекта на сервере
cd ~/myproject
git clone git@github.com:artemkuzmin72/Django-REST-framework.git .
docker-compose up -d --build