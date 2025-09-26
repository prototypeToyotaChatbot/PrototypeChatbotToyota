# syntax=docker/dockerfile:1.7

FROM node:22-alpine AS base
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=8080

COPY --from=base /app/build ./build
COPY --from=base /app/package.json ./
COPY --from=base /app/package-lock.json* ./

RUN npm install --omit=dev

EXPOSE 8080

CMD ["node", "build/index.js"]
