--
-- PostgreSQL database dump
--

\restrict Bin9oiGF7xuK2A2bOraHLcl72AoKAV1ZCGu31HkPAdlzdibKnIGCNa03juvSElj

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: strings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.strings (
    id character varying NOT NULL,
    value character varying NOT NULL,
    length integer NOT NULL,
    is_palindrome boolean NOT NULL,
    unique_characters integer NOT NULL,
    word_count integer NOT NULL,
    sha256_hash character varying NOT NULL,
    character_frequency_map json NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Data for Name: strings; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.strings (id, value, length, is_palindrome, unique_characters, word_count, sha256_hash, character_frequency_map, created_at) VALUES ('473287f8298dba7163a897908958f7c0eae733e25d2e027992ea2edc9bed2fa8', 'string', 6, false, 6, 1, '473287f8298dba7163a897908958f7c0eae733e25d2e027992ea2edc9bed2fa8', '{"s": 1, "t": 1, "r": 1, "i": 1, "n": 1, "g": 1}', '2025-10-23 08:21:22.20261+01');
INSERT INTO public.strings (id, value, length, is_palindrome, unique_characters, word_count, sha256_hash, character_frequency_map, created_at) VALUES ('e00f9ef51a95f6e854862eed28dc0f1a68f154d9f75ddd841ab00de6ede9209b', 'racecar', 7, true, 4, 1, 'e00f9ef51a95f6e854862eed28dc0f1a68f154d9f75ddd841ab00de6ede9209b', '{"r": 2, "a": 2, "c": 2, "e": 1}', '2025-10-23 08:23:41.278201+01');
INSERT INTO public.strings (id, value, length, is_palindrome, unique_characters, word_count, sha256_hash, character_frequency_map, created_at) VALUES ('2320e42e1116175c75a7cba93053734803d6ba97a7b7b4988bc29684508d9e94', 'ewe', 3, true, 2, 1, '2320e42e1116175c75a7cba93053734803d6ba97a7b7b4988bc29684508d9e94', '{"e": 2, "w": 1}', '2025-10-23 08:30:48.002116+01');


--
-- Name: strings strings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.strings
    ADD CONSTRAINT strings_pkey PRIMARY KEY (id);


--
-- Name: ix_strings_value; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_strings_value ON public.strings USING btree (value);


--
-- PostgreSQL database dump complete
--

\unrestrict Bin9oiGF7xuK2A2bOraHLcl72AoKAV1ZCGu31HkPAdlzdibKnIGCNa03juvSElj

