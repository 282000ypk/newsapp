--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: news; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.news (
    positive_vote integer,
    negative_vote integer,
    user_id text,
    news_id text
);


ALTER TABLE public.news OWNER TO postgres;

--
-- Name: newsapp_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.newsapp_user (
    id text NOT NULL,
    name character varying(40),
    email text,
    profile_pic_url text,
    type character varying(10)
);


ALTER TABLE public.newsapp_user OWNER TO postgres;

--
-- Name: user_preference; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_preference (
    id text NOT NULL,
    language character varying(10),
    country character varying(30)
);


ALTER TABLE public.user_preference OWNER TO postgres;

--
-- Data for Name: news; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.news (positive_vote, negative_vote, user_id, news_id) FROM stdin;
1	0	103393445612909473406	e9079139175b936866b85a8d6bec3781
1	0	103393445612909473406	news7460e1d7afefe6e84e9c5ae507be9f67
1	0	103393445612909473406	news8d3c03320cc6a39554bb241f18349579
1	0	103393445612909473406	newsf70b00ee460304f1649712e83d8316c9
1	0	103393445612909473406	newse9079139175b936866b85a8d6bec3781
0	1	103393445612909473406	news7655a4775e013f2bad1578be94205755
\.


--
-- Data for Name: newsapp_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.newsapp_user (id, name, email, profile_pic_url, type) FROM stdin;
test'test,'test'test'USER	\N	\N	\N	\N
test	test,	test	test	USER
103393445612909473406	Yogesh	ypk282000@gmail.com	https://lh3.googleusercontent.com/a-/AOh14Gj4Iq8aNC7FwipUUixr8ZJ20CjFkIV68JEXgMtA=s96-c	USER
115612343747350680365	Yogesh	ypkamble200045@gmail.com	https://lh3.googleusercontent.com/a-/AOh14Gi1Dmwmj3WLFutSN2h--E5v2cZM0O4lVgsBodx4Hw=s96-c	ADMIN
111404381809902874834	Nikhil	nikhil36shinde@gmail.com	https://lh3.googleusercontent.com/a/AATXAJydl4yQXjVvBtL7O7cCBSettYUoCBC6mzFSso4-=s96-c	USER
\.


--
-- Data for Name: user_preference; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_preference (id, language, country) FROM stdin;
111404381809902874834	en	in
103393445612909473406	en	in
\.


--
-- Name: newsapp_user newsapp_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.newsapp_user
    ADD CONSTRAINT newsapp_user_pkey PRIMARY KEY (id);


--
-- Name: user_preference user_preference_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_preference
    ADD CONSTRAINT user_preference_pkey PRIMARY KEY (id);


--
-- Name: news news_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.newsapp_user(id);


--
-- Name: user_preference user_preference_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_preference
    ADD CONSTRAINT user_preference_id_fkey FOREIGN KEY (id) REFERENCES public.newsapp_user(id);


--
-- PostgreSQL database dump complete
--

