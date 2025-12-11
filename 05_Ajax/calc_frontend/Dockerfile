# Use the same Node image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# COPY . . takes everything in the current folder (/frontend)
# and puts it into the container's /app folder.
# This includes webserver.js, index.html, style.css, and script.js
COPY . .

# Your webserver.js listens on port 80
EXPOSE 8080

# Run the server
CMD ["node", "webserv.js"]