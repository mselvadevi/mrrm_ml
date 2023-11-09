FROM nginx:mainline
WORKDIR usr/src/nlp
COPY . .
#COPY default.conf /etc/nginx/conf.d/default.conf
#COPY ./ssl /etc/nginx/
EXPOSE 443
CMD ["nginx", "-g", "daemon off;"]
