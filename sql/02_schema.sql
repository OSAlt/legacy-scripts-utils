SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

CREATE SCHEMA geeksabroad;

SET search_path = geeksabroad, pg_catalog;

ALTER SCHEMA geeksabroad OWNER TO postgres;

--
-- Name: user_categories; Type: TABLE; Schema: geeksabroad; Owner: postgres
--

-- CREATE TABLE user_categories (
--     user_email text NOT NULL,
--     user_category text NOT NULL
-- );


CREATE TABLE user_abroad_metadata (
    user_email text NOT NULL,
    creation_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
    country text,
    major_city text,
    geeky_events_nearby text,
    guide boolean DEFAULT FALSE,
    fluent_local_dialect boolean DEFAULT FALSE,
    camera_friendly BOOLEAN DEFAULT FALSE,
    provides_transport boolean DEFAULT FALSE,
    provides_lodging boolean DEFAULT FALSE
);

--

ALTER TABLE user_abroad_metadata OWNER TO postgres;

ALTER TABLE ONLY user_abroad_metadata
    ADD CONSTRAINT user_id_metadata___fk FOREIGN KEY (user_email) REFERENCES
    global_data.users(user_email) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY user_abroad_metadata
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_email);


