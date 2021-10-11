FROM node:14 AS frontend

WORKDIR /frontend

COPY /frontend/package* ./

RUN npm install

COPY /frontend/ ./

ARG VUE_BUILD_MODE=production
RUN npx vue-cli-service build --mode ${VUE_BUILD_MODE}

FROM python:3.8 AS server-base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

WORKDIR /server
COPY /server/Pipfile /server/Pipfile.lock ./

RUN pip install pipenv && pipenv install --system

COPY /server ./

FROM server-base AS server

COPY --from=frontend /frontend/build/dist /server/static/dist
COPY --from=frontend /frontend/build/templates/ /server/templates/vue_build/

WORKDIR /server
