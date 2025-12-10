# Start with the official Node image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json file to the container
COPY package.json .

# INSTALL EXPRESS (and other dependencies)
RUN npm install

# Copy your calculator code (server.js)
COPY . .

# Expose the port you chose (8080)
EXPOSE 8080

# Start the server
CMD ["node", "calcnode.js"]
