FROM node:lts

# Create app directory
WORKDIR /app

# Install app dependencies by copying
# package.json AND package-lock.json
COPY package*.json ./
RUN npm install

# Bundle app source
COPY . .

EXPOSE 8081

CMD ["npm", "run", "serve"]
