FROM nginx:latest

RUN rm /etc/nginx/conf.d/*

COPY ./default.conf /etc/nginx/conf.d/

EXPOSE 8085

CMD [ "nginx", "-g", "daemon off;" ]