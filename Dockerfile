FROM python:3.8 AS server-base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

WORKDIR /code
COPY /server/Pipfile /server/Pipfile.lock /code/server/

WORKDIR /code/server
RUN pip install pipenv && pipenv install --system

COPY . /code/

WORKDIR /code/server

FROM node:15-slim AS frontend-base

WORKDIR /code

COPY /frontend/package* /code/frontend/

WORKDIR /code/frontend

RUN npm install

COPY . /code/

FROM frontend-base AS frontend-prod

ENV NODE_ENV=production

RUN npm run build

FROM server-base AS server-prod

COPY --from=frontend-prod /code/server/static/dist /code/server/static/dist
COPY --from=frontend-prod /code/server/templates/pages/_vue_base.html /code/server/templates/pages/_vue_base.html
COPY --from=frontend-prod /code/server/templates/dashboard/_vue_base.html /code/server/templates/dashboard/_vue_base.html

WORKDIR /code/server