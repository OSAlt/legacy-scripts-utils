SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

CREATE SCHEMA skills;

SET search_path = skills, pg_catalog;

ALTER SCHEMA skills OWNER TO postgres;

--
-- Name: user_categories; Type: TABLE; Schema: skills; Owner: postgres
--

CREATE TABLE user_categories (
    user_email text NOT NULL,
    user_category text NOT NULL
);


ALTER TABLE user_categories OWNER TO postgres;

--
-- Name: user_programming_languages; Type: TABLE; Schema: skills; Owner: postgres
--

CREATE TABLE user_programming_languages (
    user_email text NOT NULL,
    user_language text NOT NULL,
    skillset integer,
    description text
);


ALTER TABLE user_programming_languages OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: skills; Owner: postgres
--

CREATE TABLE user_skills_metadata (
    user_email text NOT NULL,
    creation_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
    skills_details text,
    availability text,
    coder boolean DEFAULT false,
    previous_experience boolean DEFAULT false
);


ALTER TABLE user_skills_metadata OWNER TO postgres;

ALTER TABLE ONLY user_skills_metadata
    ADD CONSTRAINT user_id_metadata___fk FOREIGN KEY (user_email) REFERENCES
    global_data.users(user_email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_categories user_categories_pkey; Type: CONSTRAINT; Schema: skills; Owner: postgres
--

ALTER TABLE ONLY user_categories
    ADD CONSTRAINT user_categories_pkey PRIMARY KEY (user_email, user_category);


--
-- Name: user_programming_languages user_programming_languages_pkey; Type: CONSTRAINT; Schema: skills; Owner: postgres
--

ALTER TABLE ONLY user_programming_languages
    ADD CONSTRAINT user_programming_languages_pkey PRIMARY KEY (user_email, user_language);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: skills; Owner: postgres
--

ALTER TABLE ONLY user_skills_metadata
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_email);


--
-- Name: user_categories user_id_categories___fk; Type: FK CONSTRAINT; Schema: skills; Owner: postgres
--

ALTER TABLE ONLY user_categories
    ADD CONSTRAINT user_id_categories___fk FOREIGN KEY (user_email) REFERENCES global_data.users(user_email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_programming_languages user_programming_languages_users_user_id_fk; Type: FK CONSTRAINT; Schema: skills; Owner: postgres
--

ALTER TABLE ONLY user_programming_languages
    ADD CONSTRAINT user_programming_languages_users_user_id_fk FOREIGN KEY (user_email) REFERENCES global_data.users(user_email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

