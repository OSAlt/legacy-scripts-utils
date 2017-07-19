SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = ON;
SET check_function_bodies = FALSE;
SET client_min_messages = WARNING;
SET row_security = OFF;

CREATE SCHEMA global_data;

SET search_path = global_data, pg_catalog;

ALTER SCHEMA global_data
OWNER TO postgres;


CREATE TABLE users (
  user_email    TEXT NOT NULL,
  creation_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
  discord       TEXT
);


ALTER TABLE ONLY users
  ADD CONSTRAINT users_pkey PRIMARY KEY (user_email);

