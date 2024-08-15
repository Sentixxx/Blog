FROM node:latest

WORKDIR /frontend

COPY package.json ./

RUN npm install -g pnpm

RUN pnpm install

COPY . .

# RUN pnpm run build

# FROM nginx:latest
# COPY --from=0 /frontend/dist /usr/share/nginx/html

EXPOSE 3000


# CMD ["nginx", "-g", "daemon off;"]
CMD ["pnpm", "dev"]