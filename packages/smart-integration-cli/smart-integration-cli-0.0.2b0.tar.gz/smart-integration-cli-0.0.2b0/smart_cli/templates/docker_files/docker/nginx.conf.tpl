server {
    listen 80;
    server_name localhost;
    server_tokens off;
    access_log  /var/log/nginx/example.log;
    location /static/ {
        autoindex off;
        alias /static_files/;
    }

    location / {
        try_files $uri $uri/ @backend;
    }
    location @backend {
        proxy_pass http://python:8000;
        proxy_pass_request_headers on;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}