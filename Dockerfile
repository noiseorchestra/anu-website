FROM python:3.8 AS server-base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

WORKDIR /server
COPY /server/Pipfile /server/Pipfile.lock /server/

WORKDIR /server
RUN pip install pipenv && pipenv install --system

COPY /server /server

WORKDIR /server

FROM node:14 AS frontend-base

WORKDIR /frontend

COPY /frontend/package* /frontend/

RUN npm install

COPY /frontend/ /frontend/

FROM frontend-base AS frontend-prod

ENV NODE_ENV=production

RUN npm run build

FROM frontend-base AS frontend-dev

ENV NODE_ENV=development

RUN npm run build:dev

FROM server-base AS server-prod

COPY --from=frontend-prod /frontend/build/dist /server/static/dist
COPY --from=frontend-prod /frontend/build/templates/ /server/templates/vue_build/

WORKDIR /server

FROM server-base AS server-dev

COPY --from=frontend-dev /frontend/build/templates/ /server/templates/vue_build/

WORKDIR /server