FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build Next.js app
RUN npm run build

EXPOSE 3005

ENV PORT 3005

# Start Next.js production server
CMD ["npm", "run", "start"]
