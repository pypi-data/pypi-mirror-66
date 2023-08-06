version: '3'
volumes:
  pgdata:
services:
  python: &python # link to instance
    build:
      context: .
      dockerfile: docker/local/python/Dockerfile
    volumes:
    - ./{{params['project_name'] }}:/{{ params['project_name'] }}
    ports:
    - 8000:8000
    command: python manage.py runserver 0.0.0.0:8000
    depends_on:
      - postgres
      - rabbitmq
      - celery_worker
  postgres:
    image: postgres:10.3-alpine
    restart: always
    environment:
      POSTGRES_USER: test
      POSTGRES_DB: test
      POSTGRES_PASSWORD: test
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - 5434:5432
  rabbitmq:
    image: rabbitmq:3.7-alpine
  celery_worker:
    <<: *python # up to copy of instance
    command: celery -A {{params['project_name'] }} worker --loglevel=info
    ports: []
    depends_on:
      - postgres
      - rabbitmq
