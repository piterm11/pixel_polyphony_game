FROM node:10-alpine AS base


FROM base as development
ENV RUN_ENV=development

WORKDIR /app/
COPY package.json ./
RUN yarn install
CMD ["yarn", "run", "start"]


FROM base as production
ENV RUN_ENV=production

COPY . /app/
WORKDIR /app/
RUN yarn install
CMD ["yarn", "run", "start"]
