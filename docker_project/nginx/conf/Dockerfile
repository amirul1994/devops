# Use the nginx base image
FROM nginx:stable-alpine

# Copy the nginx configuration file to the container
COPY nginx.conf /etc/nginx/nginx.conf

# Create a new user and group for the web server to run as
RUN adduser -D -H -u 1000 -s /sbin/nologin -G www-data www-data

CMD ["nginx", "-g", "daemon off;"]