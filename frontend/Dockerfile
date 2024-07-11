FROM node:16

   WORKDIR /app

   COPY package*.json ./
   COPY tsconfig.json ./
   COPY vite.config.ts ./

   RUN npm install

   COPY . .

   RUN npm run build

   EXPOSE 3000

   CMD ["npm", "run", "dev"]