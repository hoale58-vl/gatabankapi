# Docker build

```
docker network create gatabank

docker pull mysql:5.7
docker run --name gatabank-db -e MYSQL_ROOT_PASSWORD=Admin123 \
    --network gatabank \
    -e MYSQL_DATABASE=gatabank \
    -e MYSQL_USER=gatabank \
    -e MYSQL_PASSWORD=Admin123 \
    -d mysql:5.7

docker build . -t django
docker run -it \
    --rm \
    --name gatabank-api \
    --network gatabank \
    --mount type=bind,source="$(pwd)"/gatabank,target=/app \
    -e DB_NAME=gatabank \
    -e DB_USER=gatabank \
    -e DB_PASSWORD=Admin123 \
    django \
    python manage.py makemigrations
    
docker run -it \
    --rm \
    --name gatabank-api \
    --network gatabank \
    --mount type=bind,source="$(pwd)"/gatabank,target=/app \
    -e DB_NAME=gatabank \
    -e DB_USER=gatabank \
    -e DB_PASSWORD=Admin123 \
    django \
    python manage.py migrate

```