FROM nginx:alpine

# تعديل منفذ NGINX إلى 8080 ليتوافق مع Cloud Run
RUN sed -i 's/listen  *80;/listen 8080;/g' /etc/nginx/conf.d/default.conf

COPY . /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]