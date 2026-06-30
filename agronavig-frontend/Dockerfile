# Build stage
FROM node:24-alpine as build-stage

WORKDIR /app

COPY package*.json ./
RUN npm set fetch-retries 5 \
 && npm set fetch-retry-factor 2 \
 && npm set fetch-timeout 120000 \
 && npm install

COPY . .
RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
# Copier une config nginx personnalisée pour gérer le routage React
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
