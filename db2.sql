--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.11
-- Dumped by pg_dump version 9.5.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: bookmarks; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE bookmarks (
    bookmark_id integer NOT NULL,
    user_id integer,
    etsy_listing_id integer NOT NULL
);


ALTER TABLE bookmarks OWNER TO vagrant;

--
-- Name: bookmarks_bookmark_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE bookmarks_bookmark_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE bookmarks_bookmark_id_seq OWNER TO vagrant;

--
-- Name: bookmarks_bookmark_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE bookmarks_bookmark_id_seq OWNED BY bookmarks.bookmark_id;


--
-- Name: etsyresults; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE etsyresults (
    etsy_listing_id integer NOT NULL,
    listing_title character varying(2000) NOT NULL,
    listing_url character varying(2000) NOT NULL,
    listing_image character varying(2000) NOT NULL,
    listing_price double precision
);


ALTER TABLE etsyresults OWNER TO vagrant;

--
-- Name: etsyresults_etsy_listing_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE etsyresults_etsy_listing_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE etsyresults_etsy_listing_id_seq OWNER TO vagrant;

--
-- Name: etsyresults_etsy_listing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE etsyresults_etsy_listing_id_seq OWNED BY etsyresults.etsy_listing_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE users (
    user_id integer NOT NULL,
    email character varying(64) NOT NULL,
    password character varying(64) NOT NULL,
    gender character varying(64),
    age integer,
    size character varying(64),
    pant_size integer,
    shoe_size double precision,
    pinterest_token character varying(100)
);


ALTER TABLE users OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: bookmark_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY bookmarks ALTER COLUMN bookmark_id SET DEFAULT nextval('bookmarks_bookmark_id_seq'::regclass);


--
-- Name: etsy_listing_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY etsyresults ALTER COLUMN etsy_listing_id SET DEFAULT nextval('etsyresults_etsy_listing_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: bookmarks; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY bookmarks (bookmark_id, user_id, etsy_listing_id) FROM stdin;
1	1	481372308
2	6	114325374
3	6	223956858
4	6	223956858
5	6	515315459
6	6	564722057
7	6	536060430
8	6	491617080
9	7	114325374
10	8	215364153
11	8	563221099
12	8	572395340
13	6	215364153
14	6	563839575
15	6	188495144
16	6	563839575
17	6	563839575
18	6	563839575
19	6	114325374
20	6	259685323
21	6	560411465
22	6	286721971
23	6	566076715
24	6	562709257
25	6	252152500
26	6	114325374
27	6	35449715
28	10	114325374
29	10	221863638
30	10	593546601
31	10	547805511
32	10	516375637
33	10	231595871
34	10	558847884
35	10	706332226
36	10	676945920
37	10	705968676
38	10	687876112
39	10	656266677
40	10	656266677
41	10	612286827
42	10	693704164
43	10	693704164
\.


--
-- Name: bookmarks_bookmark_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('bookmarks_bookmark_id_seq', 43, true);


--
-- Data for Name: etsyresults; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY etsyresults (etsy_listing_id, listing_title, listing_url, listing_image, listing_price) FROM stdin;
481372308	White - PLUS Size XL or Extra Plus XXL Adult, Teen, Women&#39;s 3 Layer Ballet Tutu Skirt - Three Layers, Costume	https://www.etsy.com/listing/481372308/white-plus-size-xl-or-extra-plus-xxl?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/171/0/5526407/il_170x135.1093023340_3xz4.jpg	18.9699999999999989
114325374	Vintage 1980&#39;s Black Velvet  Sweetheart Strapless Drop Waist Midi/Maxi Cocktail Dress Size S/M	https://www.etsy.com/listing/114325374/vintage-1980s-black-velvet-sweetheart?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/008/1/7262782/il_170x135.392839630_neos.jpg	62
223956858	Tiger Print Scarf	https://www.etsy.com/listing/223956858/tiger-print-scarf?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/058/0/10763648/il_170x135.732769786_468x.jpg	15
515315459	Orange Aztec Rambler Hood	https://www.etsy.com/listing/515315459/orange-aztec-rambler-hood?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/212/2/10393789/il_170x135.1426468382_qpjx.jpg	55
564722057	Infinity scarf	https://www.etsy.com/listing/564722057/infinity-scarf?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/212/0/16208806/il_170x135.1323494302_h1ft.jpg	40
536060430	OLIVIA - Light Peach Dress Blooming Dahlia Dress Bridal Dress Formal Lace Dress Ruffle Sleeve Sweetheart Vintage Swing Dance Dress	https://www.etsy.com/listing/536060430/olivia-light-peach-dress-blooming-dahlia?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/210/0/6471155/il_170x135.1267342058_9gc8.jpg	59
491617080	Vintage Sheath Dress - Green Raw Silk Sleeveless 1960s Handmade - Stunning	https://www.etsy.com/listing/491617080/vintage-sheath-dress-green-raw-silk?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/142/1/5275497/il_170x135.1121375602_kk6m.jpg	32.5
215364153	Teal LONG Floor Length Ball Gown Infinity Dress Convertible Formal Multiway Wrap Dress Bridesmaid Evening Dress	https://www.etsy.com/listing/215364153/teal-long-floor-length-ball-gown?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img1.etsystatic.com/049/1/9883262/il_170x135.699614217_bn87.jpg	49
563221099	Peacock princess dress, Little girl tutu, Birthday dress, Birthday gift for her, Dance recital, Girls princess dress, Age 6-7 year old.	https://www.etsy.com/listing/563221099/peacock-princess-dress-little-girl-tutu?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/208/1/14257761/il_170x135.1317421094_8f1a.jpg	38
572395340	Teal blue silk dress, grecian vintage silk dress by Hale Bob, party casual formal cocktail floaty summer midi dress, Empire line slip dress	https://www.etsy.com/listing/572395340/teal-blue-silk-dress-grecian-vintage?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/186/1/16140471/il_170x135.1399452250_f0i9.jpg	24
563839575	green velvet holiday dress, vintage velvet dress, Christmas party dress	https://www.etsy.com/listing/563839575/green-velvet-holiday-dress-vintage?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img1.etsystatic.com/212/1/12366532/il_170x135.1367337823_e1oe.jpg	18
188495144	Teal Grecian Lace V neck Formal Prom Evening Dress with Sleeves | Fiona	https://www.etsy.com/listing/188495144/teal-grecian-lace-v-neck-formal-prom?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img1.etsystatic.com/044/0/5587637/il_170x135.598407439_2bgd.jpg	659.950000000000045
259685323	Valentines day Gift|for|her Chunky arm knitted scarf, black infinity scarfs, gifts for mom,circular scarf, knitted cowl, women scarves	https://www.etsy.com/listing/259685323/valentines-day-giftforher-chunky-arm?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/114/0/7730806/il_170x135.885168186_9ut1.jpg	31.9899999999999984
560411465	Autumn Ripple Scarf Crochet Pattern	https://www.etsy.com/listing/560411465/autumn-ripple-scarf-crochet-pattern?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/212/0/6583221/il_170x135.1306602142_1py2.jpg	2
286721971	She Is Royal African Headwrap, kente scarves, Ankara Headwraps, kente Headwraps,	https://www.etsy.com/listing/286721971/she-is-royal-african-headwrap-kente?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img1.etsystatic.com/129/0/12188941/il_170x135.990552777_2nv1.jpg	24.9899999999999984
566076715	Women Cover Up, Caftan, Kaftan, Hand Woven, Top Tunic, Wrap, Jacket, Hand dyed clothing W2	https://www.etsy.com/listing/566076715/women-cover-up-caftan-kaftan-hand-woven?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/200/0/11197123/il_170x135.1328491478_8alu.jpg	79
562709257	Fabulous - Vintage 70s Mens 8 / Womens 9 1/2 - Made U.S.A - Leather Boots - Embellished American Eagle - Honey - Tan / Tooled	https://www.etsy.com/listing/562709257/fabulous-vintage-70s-mens-8-womens-9-12?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img1.etsystatic.com/205/0/6154601/il_170x135.1362777489_r0wq.jpg	99
252152500	Hooded Scarf, Hood Scarf, Hooded Shawl,Hoodie Scarf,  Scoodie, Reversible Infinity Scarf, Scarves For Women, Black Hood,Hooded Scarves	https://www.etsy.com/listing/252152500/hooded-scarf-hood-scarf-hooded?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img1.etsystatic.com/109/1/6726082/il_170x135.850836657_igu7.jpg	29
35449715	Black Rainbow Scarf Ribbon Handknit Scarf Includes Purple, Pink, Yellow, Blue, Green Knit Accessories Scarf for Women	https://www.etsy.com/listing/35449715/black-rainbow-scarf-ribbon-handknit?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/139/1/5218450/il_170x135.918829516_hn17.jpg	48
221863638	Blush Pink LONG Floor Length Ball Gown Maxi Infinity Dress Convertible Formal Multiway Wrap Evening Dress Bridesmaid Dress Weddings Prom	https://www.etsy.com/listing/221863638/blush-pink-long-floor-length-ball-gown?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/138/1/9883262/il_170x135.889891194_98ei.jpg	49
593546601	Infinity Dress, Burgundy Infinity Dress, Infinity Wedding Dress, Bridesmaid Infinity Dress, Infinity Cocktail Dress, Infinity Maxi Dress	https://www.etsy.com/listing/593546601/infinity-dress-burgundy-infinity-dress?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img1.etsystatic.com/199/1/13249685/il_170x135.1474109397_luel.jpg	129
547805511	Bridesmaid Dress Dusty Blue Tulle Dress,Wedding Dress,Lace Illusion Back Party Dress,Spaghetti Strap Maxi Dress,A Line Evening Dress(HS548)	https://www.etsy.com/listing/547805511/bridesmaid-dress-dusty-blue-tulle?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/217/0/6300657/il_170x135.1257835432_jzx2.jpg	128
516375637	Multi Layers Tulle Skirt with Ribbon Waistband-Peach Pink	https://www.etsy.com/listing/516375637/multi-layers-tulle-skirt-with-ribbon?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/147/0/11737321/il_170x135.1155924332_20e4.jpg	19.9899999999999984
231595871	Vintage Black Silk Midi Skirt with Beaded Gold Sequined Waist Drawstring Waist Bohemian Skirt Boho Chic Festival Hippie Gypsy Skirt S M	https://www.etsy.com/listing/231595871/vintage-black-silk-midi-skirt-with?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img1.etsystatic.com/060/0/5983585/il_170x135.764573423_awik.jpg	65
558847884	80s Vintage RIMINI Black Drape Jersey Disco Dress / Wrap Bodice with Sequins - Party Dress // Sz Med	https://www.etsy.com/listing/558847884/80s-vintage-rimini-black-drape-jersey?utm_source=etsyimagesearch&utm_medium=api&utm_campaign=api	https://img0.etsystatic.com/184/0/5116750/il_170x135.1235160966_68rg.jpg	21
706332226	Rasario Silver Sequin Midi Skirt	https://api.shopstyle.com/action/apiVisitRetailer?id=706332226&pid=uid2384-40566372-99	https://img.shopstyle-cdn.com/pim/f1/e9/f1e9d2499837ae08dc33af71f463b60b_best.jpg	1435
676945920	Polo Ralph Lauren Sequin Midi Skirt	https://api.shopstyle.com/action/apiVisitRetailer?id=676945920&pid=uid2384-40566372-99	https://img.shopstyle-cdn.com/pim/9f/11/9f11a04473f5c518c4a3d873f0b5647c_best.jpg	598
705968676	Marchesa Notte 3D Floral Embroidery Off-the-Shoulder Cocktail Dress	https://api.shopstyle.com/action/apiVisitRetailer?id=705968676&pid=uid2384-40566372-99	https://img.shopstyle-cdn.com/pim/38/c8/38c80de33f1f70d2efe25953404bc20b_best.jpg	795
687876112	Alexis Sheena Floral Lace Mini Dress	https://api.shopstyle.com/action/apiVisitRetailer?id=687876112&pid=uid2384-40566372-99	https://img.shopstyle-cdn.com/pim/e5/da/e5da06e0aa7f9843d1396b14c4a9302d_best.jpg	583
656266677	Lace and Beads Lace & Beads Tierred Tulle Skirt With Embellished Waistband	https://api.shopstyle.com/action/apiVisitRetailer?id=656266677&pid=uid2384-40566372-99	https://img.shopstyle-cdn.com/pim/59/f3/59f354d25d13247d8c3a7b2d87e9d00d_best.jpg	111
612286827	boohoo Boutique Lola Thigh Split Sequin Maxi Skirt	https://api.shopstyle.com/action/apiVisitRetailer?id=612286827&pid=uid2384-40566372-99	https://img.shopstyle-cdn.com/pim/30/a9/30a9a2677ff94622fa23ff10dbe98b71_best.jpg	51
693704164	Marc Jacobs Sequined Midi Skirt	https://api.shopstyle.com/action/apiVisitRetailer?id=693704164&pid=uid2384-40566372-99	https://img.shopstyle-cdn.com/pim/13/7a/137aab8bffe864861c2487f2849e4f94_best.jpg	745
\.


--
-- Name: etsyresults_etsy_listing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('etsyresults_etsy_listing_id_seq', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY users (user_id, email, password, gender, age, size, pant_size, shoe_size, pinterest_token) FROM stdin;
1	joe@test.com	mypass123	F	25	\N	\N	\N	\N
2	mel@test.com	$2b$12$qD5jq5UNaCXn/qI82RTzf.jLNl.3eWBaed3D8HaaljId5RZP.p31W	\N	20	X-Small	25	6	\N
3	mimi@test.com	$2b$12$n7HGAierFvEHu0sosnUOqO1aFU4tNY7PKveVc5kqYPGmCe6ALpmX.	\N	16	X-Small	23	5	\N
4	gal@test.com	$2b$12$gFB6p1SfVRzjrk1jzs/agu0fft6LFMWQcqztDDFiDpNbDkasnJP2W	\N	19	Large	28	6	\N
5	a@test.com	$2b$12$guI7TQt5jprHusf1.RZ7HeKl786kCDQ0pNza5YLZ/lSPTjSEm6ey.	\N	19	X-Small	28	5	\N
6	annie@test.com	$2b$12$ZAHQH0ERU..kk5/uJmwXneUYRAve.YIKZ5H18GQrLcqkjcG1lU8AW	\N	19	X-Small	25	8	\N
7	boo@test.com	$2b$12$FqWEHS1xcMQfknrvSuNUH.syVjPm29U55G4.ayBbfUdy/PhHVBIfS	\N	21	Medium	30	5.5	\N
8	bob@test.com	$2b$12$zCVuGinionpRXkWF1kgR7OeHSU7AbouHu6MXMPl.9Haw7soSFbNwq	\N	22	Large	30	9	\N
9	mel@gmail.com	$2b$12$WZHkZmHPd8.clyaMVZfMuec7r9/gItzSes/dRKAWSUPGriudoVpZW	\N	25	X-Small	24	7	\N
10	melody@gmail.com	$2b$12$ypxxPnX.hnSF9uRhXV9vZeEeh7gu3uRatKkOwJ0s3xP8meit1Dqr2	Female	26	X-Small	25	6.5	melodychuchu
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('users_user_id_seq', 10, true);


--
-- Name: bookmarks_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY bookmarks
    ADD CONSTRAINT bookmarks_pkey PRIMARY KEY (bookmark_id);


--
-- Name: etsyresults_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY etsyresults
    ADD CONSTRAINT etsyresults_pkey PRIMARY KEY (etsy_listing_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: bookmarks_etsy_listing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY bookmarks
    ADD CONSTRAINT bookmarks_etsy_listing_id_fkey FOREIGN KEY (etsy_listing_id) REFERENCES etsyresults(etsy_listing_id);


--
-- Name: bookmarks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY bookmarks
    ADD CONSTRAINT bookmarks_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

