# FROM postgres:latest
FROM postgres:14

RUN apt update && apt install vim -y

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=1234
ENV POSTGRES_DB=postgres

ADD ./my-postgresql.conf /etc/postgresql/my-postgresql.conf

# PostgreSQL 설정 파일에 사용자 정의 설정 파일을 포함
# RUN echo "include '/etc/postgresql/my-postgresql.conf'" >> /var/lib/postgresql/data/postgresql.conf

# EXPOSE 5432