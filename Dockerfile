FROM nginx:alpine

# 1. تعديل المنفذ لـ 8080 لتوافق Cloud Run
RUN sed -i 's/listen  *80;/listen 8080;/g' /etc/nginx/conf.d/default.conf

# 2. تفريغ المجلد الافتراضي
RUN rm -rf /usr/share/nginx/html/*

# 3. نسخ محتويات مجلد Frontend مباشرة إلى مجلد NGINX الرئيسي
COPY Frontend/ /usr/share/nginx/html/

# 4. إعطاء صلاحيات القراءة الكاملة
RUN chmod -R 755 /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]