FROM nginx:latest

#RUN mkdir -p /nginx_proxy_cache
RUN rm /etc/nginx/conf.d/default.conf

#COPY ./docker/prod/nginx/django.proxy /etc/nginx/conf.d/
COPY ./docker/prod/nginx/nginx.conf /etc/nginx/conf.d/
