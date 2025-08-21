# Start from an official Node.js base image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package files first (this allows Docker to cache the npm install step)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app will run on
EXPOSE 3000

# Command to run the application in development mode
CMD ["npm", "run", "dev"]