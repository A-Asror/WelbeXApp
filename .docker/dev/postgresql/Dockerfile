FROM postgres:latest
#FROM postgis/postgis:15-3.3

RUN apt-get update && apt-get  install -y postgresql-15-postgis-3

COPY ./.docker/dev/postgresql/init.sql /docker-entrypoint-initdb.d/
