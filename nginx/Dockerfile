FROM nginx:1.15.12-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d
COPY nginx-selfsigned.crt /etc/nginx
COPY nginx-selfsigned.key /etc/nginx