version: '3'
volumes:
  static_files:
services:
  python: &python
    build:
      context: .
      dockerfile: docker/prod/python/Dockerfile
    environment:
      - DJANGO_SETTINGS_MODULE={{ params['project_name'] }}.settings.prod
    volumes:
    - ./{{ params['project_name'] }}:/{{params['project_name']}}
    - static_files:/static_files
    ports:
    - 8000:8000
    command: gunicorn -w 4 {{ params['project_name'] }}.wsgi -b 0.0.0.0:8000
    depends_on:
      - rabbitmq
      - celery_worker
  nginx:
    build:
      context: .
      dockerfile: docker/prod/nginx/Dockerfile
    volumes:
    - static_files:/static_files
    ports:
      - 8080:80
    depends_on:
      - python
  rabbitmq:
    image: rabbitmq:3.7-alpine
  celery_worker:
    <<: *python # up to copy of instance
    command: celery -A {{params['project_name'] }} worker --loglevel=info
    ports: []
    depends_on:
      - rabbitmq
