# Use a lightweight Node image
FROM node:18-alpine

# Create app directory inside the container
WORKDIR /app

# Copy package files first (better caching for npm install)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8082

# Start the application
CMD ["npm", "start"]
