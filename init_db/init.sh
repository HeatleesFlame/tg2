#!/bin/bash
set -e

psql -v ON_ERROR_STOP=0 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE DATABASE bot;
	CREATE TABLE IF NOT EXISTS users
(
    tg_id bigint NOT NULL,
    fullname character varying(30),
    "group" character varying(10),
    phone character varying(16),
    CONSTRAINT users_pkey PRIMARY KEY (tg_id)
);
  INSERT INTO users VALUES
  (${CHEF_ID}, 'test name', 'test group', 'testphone');
EOSQL
