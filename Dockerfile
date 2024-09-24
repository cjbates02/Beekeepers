# Use the official Nginx image from Docker Hub
FROM nginx:latest

# Copy the website files into the default Nginx public directory
COPY . /usr/share/nginx/html

# Expose port 80 to access the website
EXPOSE 80
