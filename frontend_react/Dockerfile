FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5173
# Ajuste para que Vite responda en Docker
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]