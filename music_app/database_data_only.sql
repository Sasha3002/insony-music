--
-- PostgreSQL database dump
--

\restrict Mqlrf3jD8gDCchmbq1zrJcL4Dni6OXeoWllbSid0L180CzsMaXwSvsAQUW0BmEE

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

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

--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: musicuser
--

SET SESSION AUTHORIZATION DEFAULT;

ALTER TABLE public.auth_group DISABLE TRIGGER ALL;

COPY public.auth_group (id, name) FROM stdin;
\.


ALTER TABLE public.auth_group ENABLE TRIGGER ALL;

--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.django_content_type DISABLE TRIGGER ALL;

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	users	user
7	authtoken	token
8	authtoken	tokenproxy
9	music	artist
10	music	track
11	music	genre
12	music	review
13	music	reviewlike
14	music	favorite
15	music	playlist
16	music	playlisttrack
17	users	userfollow
18	users	userblock
19	users	errorreport
20	chat	chatparticipant
21	chat	conversation
22	chat	messageread
23	chat	message
24	groups	groupmembership
25	groups	group
26	groups	groupinvitation
27	chat	groupchatmessage
28	chat	groupchatread
29	events	event
30	events	eventattendee
31	events	eventrating
32	events	eventpoll
33	events	pollvote
\.


ALTER TABLE public.django_content_type ENABLE TRIGGER ALL;

--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.auth_permission DISABLE TRIGGER ALL;

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add user	6	add_user
22	Can change user	6	change_user
23	Can delete user	6	delete_user
24	Can view user	6	view_user
25	Can add Token	7	add_token
26	Can change Token	7	change_token
27	Can delete Token	7	delete_token
28	Can view Token	7	view_token
29	Can add Token	8	add_tokenproxy
30	Can change Token	8	change_tokenproxy
31	Can delete Token	8	delete_tokenproxy
32	Can view Token	8	view_tokenproxy
33	Can add artist	9	add_artist
34	Can change artist	9	change_artist
35	Can delete artist	9	delete_artist
36	Can view artist	9	view_artist
37	Can add track	10	add_track
38	Can change track	10	change_track
39	Can delete track	10	delete_track
40	Can view track	10	view_track
41	Can add genre	11	add_genre
42	Can change genre	11	change_genre
43	Can delete genre	11	delete_genre
44	Can view genre	11	view_genre
45	Can add review	12	add_review
46	Can change review	12	change_review
47	Can delete review	12	delete_review
48	Can view review	12	view_review
49	Can add review like	13	add_reviewlike
50	Can change review like	13	change_reviewlike
51	Can delete review like	13	delete_reviewlike
52	Can view review like	13	view_reviewlike
53	Can add favorite	14	add_favorite
54	Can change favorite	14	change_favorite
55	Can delete favorite	14	delete_favorite
56	Can view favorite	14	view_favorite
57	Can add playlist	15	add_playlist
58	Can change playlist	15	change_playlist
59	Can delete playlist	15	delete_playlist
60	Can view playlist	15	view_playlist
61	Can add playlist track	16	add_playlisttrack
62	Can change playlist track	16	change_playlisttrack
63	Can delete playlist track	16	delete_playlisttrack
64	Can view playlist track	16	view_playlisttrack
65	Can add user follow	17	add_userfollow
66	Can change user follow	17	change_userfollow
67	Can delete user follow	17	delete_userfollow
68	Can view user follow	17	view_userfollow
69	Can add user block	18	add_userblock
70	Can change user block	18	change_userblock
71	Can delete user block	18	delete_userblock
72	Can view user block	18	view_userblock
73	Can add error report	19	add_errorreport
74	Can change error report	19	change_errorreport
75	Can delete error report	19	delete_errorreport
76	Can view error report	19	view_errorreport
77	Can add chat participant	20	add_chatparticipant
78	Can change chat participant	20	change_chatparticipant
79	Can delete chat participant	20	delete_chatparticipant
80	Can view chat participant	20	view_chatparticipant
81	Can add conversation	21	add_conversation
82	Can change conversation	21	change_conversation
83	Can delete conversation	21	delete_conversation
84	Can view conversation	21	view_conversation
85	Can add message read	22	add_messageread
86	Can change message read	22	change_messageread
87	Can delete message read	22	delete_messageread
88	Can view message read	22	view_messageread
89	Can add message	23	add_message
90	Can change message	23	change_message
91	Can delete message	23	delete_message
92	Can view message	23	view_message
93	Can add group membership	24	add_groupmembership
94	Can change group membership	24	change_groupmembership
95	Can delete group membership	24	delete_groupmembership
96	Can view group membership	24	view_groupmembership
97	Can add group	25	add_group
98	Can change group	25	change_group
99	Can delete group	25	delete_group
100	Can view group	25	view_group
101	Can add group invitation	26	add_groupinvitation
102	Can change group invitation	26	change_groupinvitation
103	Can delete group invitation	26	delete_groupinvitation
104	Can view group invitation	26	view_groupinvitation
105	Can add group chat message	27	add_groupchatmessage
106	Can change group chat message	27	change_groupchatmessage
107	Can delete group chat message	27	delete_groupchatmessage
108	Can view group chat message	27	view_groupchatmessage
109	Can add group chat read	28	add_groupchatread
110	Can change group chat read	28	change_groupchatread
111	Can delete group chat read	28	delete_groupchatread
112	Can view group chat read	28	view_groupchatread
113	Can add event	29	add_event
114	Can change event	29	change_event
115	Can delete event	29	delete_event
116	Can view event	29	view_event
117	Can add event attendee	30	add_eventattendee
118	Can change event attendee	30	change_eventattendee
119	Can delete event attendee	30	delete_eventattendee
120	Can view event attendee	30	view_eventattendee
121	Can add event rating	31	add_eventrating
122	Can change event rating	31	change_eventrating
123	Can delete event rating	31	delete_eventrating
124	Can view event rating	31	view_eventrating
125	Can add event poll	32	add_eventpoll
126	Can change event poll	32	change_eventpoll
127	Can delete event poll	32	delete_eventpoll
128	Can view event poll	32	view_eventpoll
129	Can add poll vote	33	add_pollvote
130	Can change poll vote	33	change_pollvote
131	Can delete poll vote	33	delete_pollvote
132	Can view poll vote	33	view_pollvote
\.


ALTER TABLE public.auth_permission ENABLE TRIGGER ALL;

--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.auth_group_permissions DISABLE TRIGGER ALL;

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


ALTER TABLE public.auth_group_permissions ENABLE TRIGGER ALL;

--
-- Data for Name: users_user; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.users_user DISABLE TRIGGER ALL;

COPY public.users_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, favorite_genres, favorite_artists, bio, xp, profile_picture, email_verification_sent_at, email_verification_token, is_email_verified, city) FROM stdin;
1	pbkdf2_sha256$1000000$KXiDmi1motxvGYSfKDDFAw$dTJRNkp2mh0e+n4B3gpzONHHC49EJRL03yeZSEGJwvY=	2025-10-06 15:24:56.498337+00	f	testuser			test@example.com	f	t	2025-10-01 19:15:44.106946+00	Rock	Rock	Rock	10	\N	\N	\N	f	\N
16	pbkdf2_sha256$1000000$GWNiasw26qvRIHT46V1oYE$2BpOdgi1KzjNWHA0b8OJQAEh74bQDpMvNi2In20tCV4=	2025-12-23 01:05:55.657189+00	f	Oleksandr1	Oleksandr	Konovalenko	mainsono627@gmail.com	f	t	2025-11-20 22:13:14.642517+00	emo rap, Blues, Hard Rock	IVOXYGEN, Bones, Playboi Carti	Regular user	390	profile_pics/7777.jfif	2025-11-20 22:13:15.068921+00	\N	t	Warszawa
5	pbkdf2_sha256$1000000$W5xX5KBpaVeSsc8AcviwUZ$hh/4pcw4XW5Ircks6pvGrxOslZAt19+Vqt+VY0jL8+M=	2026-01-14 02:11:03.284045+00	f	test2			test2@gmail.com	f	t	2025-10-17 22:05:17.957604+00		Slavik, Drevo	clown	0		\N	\N	f	\N
8	pbkdf2_sha256$1000000$QY6TnuuIXEoQLpAniGasVE$s4+dwp2ng05So4czFnYJwQJ08FaGGAR4wL06yXtCuVI=	2025-10-29 12:16:56.580766+00	f	Sono222			test5@gmail.com	f	t	2025-10-29 12:16:21.488896+00				0	\N	\N	\N	f	\N
2	pbkdf2_sha256$1000000$hLwhnCi1YFblKW1lG90kB2$vM7bJmeVleddBPJPEtvuGwCnKsEMQuJ6Se9CHiVVo5g=	2025-12-29 15:00:54.470956+00	f	test1			test1@gmail	f	t	2025-10-06 16:12:38.143889+00	Lo-fi, New Wave	Drevo, IVOXYGEN	test1	20	profile_pics/11.jfif	\N	\N	f	Warszawa
4	pbkdf2_sha256$1000000$ZEYv90xWYTbihN5KHzY5AI$DfuxiFeu8gznWOmhxSHmtDlwA9pt6dw+ES/M9/LxdDI=	2025-10-06 16:27:28.716323+00	f	slavik			slavikpiwo@gmail.com	f	t	2025-10-06 16:27:28.324285+00	metal	Drevo	dota2 player	10	\N	\N	\N	f	\N
10	pbkdf2_sha256$1000000$Xy4yItCzjCOy3hh9TgZafC$WWD+PfCOq8XZDhb8/C1MUbNWv6oCPoHZ8LsMuE0yiAk=	2025-11-10 01:01:26.853815+00	f	emailtest			sashakonovalenko627@gmail.com	f	t	2025-11-10 00:59:01.758736+00				0		2025-11-10 00:59:02.214456+00	\N	t	\N
3	pbkdf2_sha256$1000000$6gTZi3Y6oZL16H2XcGAnxS$FpVGwuKuWPL7dbwbKDI022/7+DkyWmLQxVVXENcIQWQ=	2026-01-06 22:37:09.142825+00	t	admin	admin	admin	admin@example.com	t	t	2025-10-06 16:17:07.803598+00	Emo-Rap, emo rap, Emo	IVOXYGEN, The Neighbourhood	Admin	3100	profile_pics/profile.jfif	\N	\N	f	Żerniki Małe
7	pbkdf2_sha256$1000000$6gNFL8cWZmwWBrVG5D3gp2$i4lgtOMKXp3VumJmAoYKtfXvcUGbZwlJoCQX0nCR/tI=	2025-10-21 22:35:20.023228+00	f	Sono			sasako@gmail.com	f	t	2025-10-21 22:35:19.456511+00				10	\N	\N	\N	f	\N
\.


ALTER TABLE public.users_user ENABLE TRIGGER ALL;

--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.authtoken_token DISABLE TRIGGER ALL;

COPY public.authtoken_token (key, created, user_id) FROM stdin;
\.


ALTER TABLE public.authtoken_token ENABLE TRIGGER ALL;

--
-- Data for Name: chat_conversation; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.chat_conversation DISABLE TRIGGER ALL;

COPY public.chat_conversation (id, type, created_at, updated_at, group_name) FROM stdin;
1	direct	2025-11-11 13:25:38.434772+00	2025-11-11 13:37:32.369239+00	\N
3	direct	2025-11-11 14:04:59.013232+00	2025-11-11 14:05:04.839512+00	\N
4	direct	2025-11-18 14:24:49.186931+00	2025-11-18 14:24:49.186931+00	\N
6	direct	2025-11-21 16:15:00.014552+00	2025-11-21 16:15:42.330672+00	\N
7	direct	2025-11-21 16:16:29.006978+00	2025-11-21 16:16:31.890458+00	\N
5	direct	2025-11-20 22:19:27.320091+00	2025-12-10 22:40:47.591899+00	\N
2	direct	2025-11-11 13:41:26.380764+00	2025-12-23 01:10:22.234423+00	\N
\.


ALTER TABLE public.chat_conversation ENABLE TRIGGER ALL;

--
-- Data for Name: chat_chatparticipant; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.chat_chatparticipant DISABLE TRIGGER ALL;

COPY public.chat_chatparticipant (id, joined_at, last_read_at, user_id, conversation_id) FROM stdin;
14	2025-11-21 16:16:29.00998+00	2025-11-28 16:08:23.971966+00	3	7
3	2025-11-11 13:41:26.381764+00	2025-12-22 02:15:47.533815+00	2	2
8	2025-11-18 14:24:49.189993+00	2025-11-18 14:25:43.463931+00	3	4
5	2025-11-11 14:04:59.014481+00	2025-12-23 01:35:01.420133+00	3	3
6	2025-11-11 14:04:59.014481+00	\N	4	3
11	2025-11-21 16:15:00.015553+00	2026-01-06 23:37:55.876022+00	3	6
10	2025-11-20 22:19:27.321091+00	2026-01-06 23:40:41.684387+00	3	5
4	2025-11-11 13:41:26.382765+00	2026-01-07 16:06:08.057483+00	3	2
9	2025-11-20 22:19:27.321091+00	2025-11-21 15:50:25.36937+00	16	5
2	2025-11-11 13:25:38.436774+00	2025-11-21 15:50:47.227205+00	5	1
1	2025-11-11 13:25:38.435773+00	2025-11-21 15:50:52.05881+00	3	1
12	2025-11-21 16:15:00.016554+00	\N	10	6
\.


ALTER TABLE public.chat_chatparticipant ENABLE TRIGGER ALL;

--
-- Data for Name: groups_group; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.groups_group DISABLE TRIGGER ALL;

COPY public.groups_group (id, name, slug, description, location, cover_image, type, created_at, updated_at, admin_id) FROM stdin;
1	Jazz w Warszawie	jazz-w-warszawie	Join to us 	Warszawa	group_covers/group_pic.jfif	private	2025-11-11 22:28:08.2565+00	2025-11-14 14:22:35.061802+00	3
3	Hip-Hop Collective	hip-hop-collective	Społeczność miłośników hip-hopu w Warszawie. Organizujemy jam sessions, bitmakingi i koncerty lokalnych artystów.	Warszawa	group_covers/26880929020578935.jfif	public	2025-11-17 23:43:38.947475+00	2025-11-17 23:43:38.947475+00	3
4	Jazz Society	jazz-society	Grupa dla fanów jazzu i improwizacji. Spotykamy się w klubach jazzowych, dyskutujemy o klasykach i nowych talentach.	Kraków	group_covers/Коты.jfif	private	2025-11-17 23:52:20.307842+00	2025-11-17 23:52:20.307842+00	3
5	Electronic Beats	electronic-beats	Pasjonaci muzyki elektronicznej. Od techno po ambient - dzielimy się produkcjami i organizujemy warehouse parties.	Poznań	group_covers/Без_названия.jfif	public	2025-11-17 23:53:05.94607+00	2025-11-17 23:53:05.94607+00	3
6	Rock Rebels	rock-rebels	Rockowa rodzina Wrocławia. Koncerty, jam sessions i wspólne granie w próbowniach.	Wrocław	group_covers/Без_названия_1.jfif	public	2025-11-17 23:53:57.530302+00	2025-11-17 23:53:57.530302+00	3
7	Reggae Vibes	reggae-vibes	Good vibes only! Miłośnicy reggae, dub i ska. Organizujemy soundsystemy i festiwale plenerowe.	Gdańsk	group_covers/Walpappers.jfif	public	2025-11-17 23:54:49.515667+00	2025-11-17 23:54:49.515667+00	3
8	Underground	underground	Eksperymentalna scena Łodzi. Dla tych, którzy szukają czegoś poza mainstreamem.	Łódź	group_covers/Без_названия_2.jfif	public	2025-11-17 23:56:53.202449+00	2025-11-17 23:56:53.202449+00	3
10	Boom Bap Society	boom-bap-society	Dla fanów oldschoolowego hip-hopu. Samplingi, breaki i złota era rap game.	Warszawa	group_covers/Без_названия_4.jfif	public	2025-11-20 19:10:35.868379+00	2025-11-20 19:10:35.868379+00	2
11	Kraków Electronic Experiments	krakow-electronic-experiments	Laboratoria dźwięku. Modular synths, live coding i eksperymenty soniczne.	Kraków 	group_covers/Spike_Spiegel.jfif	public	2025-11-20 22:22:38.097446+00	2025-11-20 22:22:38.097446+00	16
9	Tri-City Indie Collectived	tri-city-indie-collective	Indie scena Trójmiasta. Wspieramy lokalne zespoły i organizujemy intimate shows.	Gdynia	group_covers/Без_названия_3.jfif	private	2025-11-17 23:59:17.56781+00	2025-12-23 01:51:36.398879+00	3
\.


ALTER TABLE public.groups_group ENABLE TRIGGER ALL;

--
-- Data for Name: chat_groupchatmessage; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.chat_groupchatmessage DISABLE TRIGGER ALL;

COPY public.chat_groupchatmessage (id, content, created_at, edited_at, is_edited, group_id, sender_id) FROM stdin;
12	ghg	2025-11-20 19:11:04.726773+00	\N	f	10	3
13	fghf	2025-11-20 19:11:09.683335+00	\N	f	10	2
15	Hi again	2025-11-20 22:23:13.874669+00	\N	f	11	16
16	hi bro	2025-11-20 22:25:51.110346+00	\N	f	11	3
18	SADDASDAS	2025-12-22 17:22:17.941615+00	\N	f	1	3
19	asdasdasda	2025-12-22 17:22:44.658594+00	\N	f	1	2
23	ghgh	2026-01-14 02:49:24.185197+00	\N	f	9	3
\.


ALTER TABLE public.chat_groupchatmessage ENABLE TRIGGER ALL;

--
-- Data for Name: chat_groupchatread; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.chat_groupchatread DISABLE TRIGGER ALL;

COPY public.chat_groupchatread (id, last_read_at, group_id, user_id) FROM stdin;
7	2025-11-20 19:11:07.062028+00	10	2
8	2025-11-20 22:22:59.191615+00	11	16
10	2025-11-21 15:35:07.561878+00	5	3
9	2025-12-01 17:43:56.172889+00	11	3
12	2025-12-22 17:21:58.769461+00	3	3
6	2025-12-22 17:22:04.348356+00	10	3
2	2025-12-22 17:27:56.68303+00	1	2
13	2026-01-07 15:36:37.486666+00	4	3
1	2026-01-07 15:36:45.901615+00	1	3
14	2026-01-07 15:37:09.071132+00	1	5
11	2026-01-14 02:45:43.091171+00	9	3
\.


ALTER TABLE public.chat_groupchatread ENABLE TRIGGER ALL;

--
-- Data for Name: chat_message; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.chat_message DISABLE TRIGGER ALL;

COPY public.chat_message (id, content, created_at, edited_at, is_edited, conversation_id, sender_id) FROM stdin;
1	wqe	2025-11-11 13:25:54.624384+00	\N	f	1	3
2	asdas	2025-11-11 13:26:00.277872+00	\N	f	1	3
3	asdsad	2025-11-11 13:26:01.752038+00	\N	f	1	3
4	fdsf	2025-11-11 13:37:27.710313+00	\N	f	1	3
5	sfsdfsdfsd	2025-11-11 13:37:29.944148+00	\N	f	1	3
6	hio	2025-11-11 13:37:32.368237+00	\N	f	1	3
7	hi	2025-11-11 13:41:29.367816+00	\N	f	2	2
8	you	2025-11-11 13:41:42.826848+00	\N	f	2	3
9	jhkhjk	2025-11-11 13:42:04.608428+00	\N	f	2	2
10	hi	2025-11-11 14:05:01.915142+00	\N	f	3	3
11	slavik	2025-11-11 14:05:04.835818+00	\N	f	3	3
12	dfsf	2025-11-11 14:11:59.248433+00	\N	f	2	3
13	zczxczxc	2025-11-11 14:12:43.165904+00	\N	f	2	2
14	you	2025-11-11 14:17:20.088141+00	\N	f	2	2
15	nice one	2025-11-11 14:17:28.263542+00	\N	f	2	2
16	ww	2025-11-11 14:18:10.22964+00	\N	f	2	2
17	sad	2025-11-11 14:25:38.619197+00	\N	f	2	3
18	try this	2025-11-11 14:26:10.675598+00	\N	f	2	2
19	kys	2025-11-11 14:28:44.604372+00	\N	f	2	2
20	wtf	2025-11-11 14:29:25.11992+00	\N	f	2	2
21	dfgdfg	2025-11-11 14:33:52.245623+00	\N	f	2	2
22	http://127.0.0.1:8000/users/profile/	2025-11-11 14:41:13.406658+00	\N	f	2	3
23	sdfsd	2025-11-11 14:41:46.455234+00	\N	f	2	2
24	kl;k;l	2025-11-11 14:41:52.208339+00	\N	f	2	2
25	sd	2025-11-11 14:43:14.873704+00	\N	f	2	2
26	fg	2025-11-11 14:43:15.143261+00	\N	f	2	2
27	gdsf	2025-11-11 14:43:15.357068+00	\N	f	2	2
28	gdsf	2025-11-11 14:43:15.558088+00	\N	f	2	2
29	g	2025-11-11 14:43:15.847499+00	\N	f	2	2
30	df	2025-11-11 14:43:16.092708+00	\N	f	2	2
31	sd	2025-11-11 14:43:16.260681+00	\N	f	2	2
32	h	2025-11-11 14:43:16.561909+00	\N	f	2	2
33	fd	2025-11-11 14:43:16.815294+00	\N	f	2	2
34	df	2025-11-11 14:43:16.990696+00	\N	f	2	2
35	h	2025-11-11 14:43:17.281667+00	\N	f	2	2
36	df	2025-11-11 14:43:17.51763+00	\N	f	2	2
37	df	2025-11-11 14:43:17.661139+00	\N	f	2	2
38	h	2025-11-11 14:43:17.953678+00	\N	f	2	2
39	df	2025-11-11 14:43:18.296695+00	\N	f	2	2
40	hdf	2025-11-11 14:43:18.518495+00	\N	f	2	2
41	h	2025-11-11 14:43:20.252849+00	\N	f	2	2
42	qq	2025-11-11 15:17:55.979836+00	\N	f	2	2
43	asdasda	2025-11-11 15:18:13.510732+00	\N	f	2	2
44	l;'l;'l;	2025-11-11 15:18:17.279588+00	\N	f	2	2
45	ww	2025-11-11 15:18:28.707874+00	\N	f	2	3
46	5etre	2025-11-11 15:18:39.181525+00	\N	f	2	3
47	hgjghjgh	2025-11-11 15:18:46.137173+00	\N	f	2	3
48	asdas	2025-11-19 23:23:19.724303+00	\N	f	2	3
49	sda	2025-11-19 23:24:00.786892+00	\N	f	2	2
50	HI	2025-11-20 22:19:29.635095+00	\N	f	5	16
51	lets be friends	2025-11-20 22:19:38.443483+00	\N	f	5	16
52	Ok	2025-11-20 22:25:59.331392+00	\N	f	5	3
53	asdasd	2025-11-21 16:15:42.32778+00	\N	f	6	3
55	hi	2025-12-10 22:40:47.587916+00	\N	f	5	3
56	adasd	2025-12-22 01:58:02.401934+00	\N	f	2	2
57	sdfsdfdsf	2025-12-22 01:59:25.643782+00	\N	f	2	2
58	asdas	2025-12-22 02:05:08.280089+00	\N	f	2	2
59	sdfsdfsdf	2025-12-22 02:05:53.969732+00	\N	f	2	2
60	asdada	2025-12-22 02:07:02.87817+00	\N	f	2	2
61	asdasd	2025-12-22 02:15:49.626788+00	\N	f	2	2
62	ffg	2025-12-22 19:26:22.886557+00	\N	f	2	3
63	ki	2025-12-22 19:32:26.869027+00	\N	f	2	3
\.


ALTER TABLE public.chat_message ENABLE TRIGGER ALL;

--
-- Data for Name: chat_messageread; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.chat_messageread DISABLE TRIGGER ALL;

COPY public.chat_messageread (id, read_at, message_id, user_id) FROM stdin;
\.


ALTER TABLE public.chat_messageread ENABLE TRIGGER ALL;

--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.django_admin_log DISABLE TRIGGER ALL;

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2025-10-17 21:00:34.570356+00	1	Drevo	1	[{"added": {}}]	9	3
2	2025-10-17 21:00:42.087984+00	1	Rock	1	[{"added": {}}]	11	3
3	2025-10-29 19:53:25.457179+00	4	Smaragdove Nebo - Drevo · admin · 5/5	3		12	3
4	2025-10-29 19:53:29.428247+00	3	Smaragdove Nebo - Drevo · test1 · 4/5	3		12	3
5	2025-10-29 19:53:33.604608+00	1	Smaragdove Nebo - Drevo · Sono222 · 1/5	3		12	3
6	2025-10-29 23:04:32.090563+00	2	IVOXYGEN	1	[{"added": {}}]	9	3
7	2025-10-29 23:05:16.470384+00	2	hip-hop	1	[{"added": {}}]	11	3
8	2025-10-29 23:05:30.273934+00	3	emo rap	1	[{"added": {}}]	11	3
9	2025-10-29 23:06:04.877358+00	2	Young KId - IVOXYGEN	1	[{"added": {}}]	10	3
10	2025-10-29 23:07:18.511436+00	3	suisside	1	[{"added": {}}]	9	3
11	2025-10-29 23:07:29.415069+00	3	Dark side of the moon - suisside	1	[{"added": {}}]	10	3
12	2025-10-30 22:00:21.560524+00	7	Young KId - IVOXYGEN · admin · 38/60 (63.3%)	2	[]	12	3
13	2025-10-30 22:00:39.548353+00	9	Young KId - IVOXYGEN · slavik · 18/60 (30.0%)	1	[{"added": {}}]	12	3
14	2025-10-30 22:00:52.47847+00	10	Young KId - IVOXYGEN · Sono · 30/60 (50.0%)	1	[{"added": {}}]	12	3
15	2025-10-30 22:01:06.913636+00	11	Young KId - IVOXYGEN · Sono222 · 42/60 (70.0%)	1	[{"added": {}}]	12	3
16	2025-10-30 22:01:21.206164+00	12	Young KId - IVOXYGEN · test1 · 54/60 (90.0%)	1	[{"added": {}}]	12	3
17	2025-10-30 22:01:43.986617+00	13	Young KId - IVOXYGEN · test2 · 6/60 (10.0%)	1	[{"added": {}}]	12	3
18	2025-10-30 22:01:56.546609+00	14	Young KId - IVOXYGEN · test3 · 48/60 (80.0%)	1	[{"added": {}}]	12	3
19	2025-10-30 22:02:13.034601+00	15	Young KId - IVOXYGEN · testuser · 36/60 (60.0%)	1	[{"added": {}}]	12	3
20	2025-10-31 12:52:17.248397+00	2	Young KId - IVOXYGEN	2	[{"changed": {"fields": ["Data utworu (autora)", "Czas trwania"]}}]	10	3
21	2025-10-31 21:34:14.033357+00	33	nothing to u - Lil Peep	2	[{"changed": {"fields": ["Genre"]}}]	10	3
22	2025-10-31 22:20:18.003827+00	8	Pop	1	[{"added": {}}]	11	3
23	2025-10-31 22:20:26.241785+00	9	Rap	1	[{"added": {}}]	11	3
24	2025-10-31 22:20:29.889865+00	10	R&B	1	[{"added": {}}]	11	3
25	2025-10-31 22:20:32.789718+00	11	Soul	1	[{"added": {}}]	11	3
26	2025-10-31 22:20:35.96677+00	12	Jazz	1	[{"added": {}}]	11	3
27	2025-10-31 22:20:38.878865+00	13	Blues	1	[{"added": {}}]	11	3
28	2025-10-31 22:20:42.187857+00	14	Classical	1	[{"added": {}}]	11	3
29	2025-10-31 22:20:45.300642+00	15	EDM	1	[{"added": {}}]	11	3
30	2025-10-31 22:20:50.716728+00	16	House	1	[{"added": {}}]	11	3
31	2025-10-31 22:20:55.504583+00	17	Techno	1	[{"added": {}}]	11	3
32	2025-10-31 22:20:59.210734+00	18	Dubstep	1	[{"added": {}}]	11	3
33	2025-10-31 22:21:02.020666+00	19	Drum & Bass	1	[{"added": {}}]	11	3
34	2025-10-31 22:21:04.479546+00	20	Reggae	1	[{"added": {}}]	11	3
35	2025-10-31 22:21:07.810088+00	21	Dancehall	1	[{"added": {}}]	11	3
36	2025-10-31 22:21:10.919413+00	22	Afrobeat	1	[{"added": {}}]	11	3
37	2025-10-31 22:21:13.534458+00	23	Latin	1	[{"added": {}}]	11	3
38	2025-10-31 22:21:16.343353+00	24	Reggaeton	1	[{"added": {}}]	11	3
39	2025-10-31 22:21:18.988438+00	25	Country	1	[{"added": {}}]	11	3
40	2025-10-31 22:21:21.386715+00	26	Folk	1	[{"added": {}}]	11	3
41	2025-10-31 22:21:23.943408+00	27	Indie	1	[{"added": {}}]	11	3
42	2025-10-31 22:21:28.093408+00	28	Alternative	1	[{"added": {}}]	11	3
43	2025-10-31 22:21:31.326182+00	29	Metal	1	[{"added": {}}]	11	3
44	2025-10-31 22:21:34.503711+00	30	Heavy Metal	1	[{"added": {}}]	11	3
45	2025-10-31 22:21:38.179493+00	31	Punk	1	[{"added": {}}]	11	3
46	2025-10-31 22:21:41.010201+00	32	Emo	1	[{"added": {}}]	11	3
47	2025-10-31 22:21:44.937258+00	33	Funk	1	[{"added": {}}]	11	3
48	2025-10-31 22:21:47.314877+00	34	Disco	1	[{"added": {}}]	11	3
49	2025-10-31 22:21:50.053707+00	35	K-pop	1	[{"added": {}}]	11	3
50	2025-10-31 22:21:52.993448+00	36	J-pop	1	[{"added": {}}]	11	3
51	2025-10-31 22:21:55.801763+00	37	C-pop	1	[{"added": {}}]	11	3
52	2025-10-31 22:21:58.624573+00	38	Lo-fi	1	[{"added": {}}]	11	3
53	2025-10-31 22:22:01.676174+00	39	Ambient	1	[{"added": {}}]	11	3
54	2025-10-31 22:22:05.019293+00	40	Soundtrack / Score	1	[{"added": {}}]	11	3
55	2025-10-31 22:22:09.022277+00	41	Gospel	1	[{"added": {}}]	11	3
56	2025-10-31 22:22:11.761119+00	42	Opera	1	[{"added": {}}]	11	3
57	2025-10-31 22:22:15.683143+00	43	Dance-Pop	1	[{"added": {}}]	11	3
58	2025-10-31 22:22:18.26244+00	44	Trap	1	[{"added": {}}]	11	3
59	2025-10-31 22:22:20.801565+00	45	Drill	1	[{"added": {}}]	11	3
60	2025-10-31 22:22:23.631874+00	46	Ska	1	[{"added": {}}]	11	3
61	2025-10-31 22:22:26.944201+00	47	Synth-pop	1	[{"added": {}}]	11	3
62	2025-10-31 22:22:29.676038+00	48	New Wave	1	[{"added": {}}]	11	3
63	2025-10-31 22:22:32.476554+00	49	Grunge	1	[{"added": {}}]	11	3
64	2025-10-31 22:22:35.883456+00	50	Soft Rock	1	[{"added": {}}]	11	3
65	2025-10-31 22:22:38.447954+00	51	Hard Rock	1	[{"added": {}}]	11	3
66	2025-10-31 22:22:52.587423+00	52	World Music	1	[{"added": {}}]	11	3
67	2025-10-31 22:35:36.154691+00	72	Utterance Beyond Death - Bones	2	[{"changed": {"fields": ["Genre"]}}]	10	3
68	2025-10-31 22:35:56.016678+00	71	Execration Rites - Bones	2	[{"changed": {"fields": ["Genre"]}}]	10	3
69	2025-10-31 22:37:39.707403+00	70	Deserts of Eternity - Bones	2	[{"changed": {"fields": ["Genre"]}}]	10	3
70	2025-10-31 22:38:12.359274+00	69	1000 Lies - Bones	2	[{"changed": {"fields": ["Genre"]}}]	10	3
71	2025-10-31 22:38:32.208907+00	18	Tiptoe - Imagine Dragons	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
72	2025-10-31 22:38:51.524595+00	17	Amsterdam - Imagine Dragons	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
73	2025-10-31 22:39:15.796735+00	16	Cha‐Ching (Till We Grow Older) - Imagine Dragons	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
74	2025-10-31 22:39:33.050644+00	15	Monster - Imagine Dragons	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
75	2025-10-31 22:41:54.745725+00	9	My Fault - Imagine Dragons	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
76	2025-10-31 22:42:24.691021+00	1	Smaragdove Nebo - Drevo	2	[{"changed": {"fields": ["Data utworu (autora)", "Czas trwania"]}}]	10	3
77	2025-10-31 22:43:18.516591+00	68	Untitled - Bones	2	[{"changed": {"fields": ["Genre"]}}]	10	3
78	2025-10-31 22:43:28.296148+00	67	Us - BONES UK	2	[{"changed": {"fields": ["Genre"]}}]	10	3
79	2025-10-31 22:43:37.131634+00	66	Bikinis - BONES UK	2	[{"changed": {"fields": ["Genre"]}}]	10	3
80	2025-10-31 22:43:43.256121+00	65	Visions - Bones	2	[{"changed": {"fields": ["Genre"]}}]	10	3
81	2025-10-31 22:43:52.072324+00	64	Driving Me Wild - Bones	2	[{"changed": {"fields": ["Genre"]}}]	10	3
82	2025-10-31 22:44:02.367964+00	63	Cyclopean Edifice - Bones	2	[{"changed": {"fields": ["Genre"]}}]	10	3
83	2025-10-31 22:44:09.629441+00	62	The View From the Afternoon - Arctic Monkeys	2	[{"changed": {"fields": ["Genre"]}}]	10	3
84	2025-10-31 22:44:16.738464+00	61	Mardy Bum - Arctic Monkeys	2	[{"changed": {"fields": ["Genre"]}}]	10	3
85	2025-10-31 22:44:25.516458+00	55	Perhaps Vampires Is a Bit Strong But... - Arctic Monkeys	2	[{"changed": {"fields": ["Genre"]}}]	10	3
86	2025-10-31 22:44:42.258426+00	54	Bigger Boys and Stolen Sweethearts - Arctic Monkeys	2	[{"changed": {"fields": ["Genre"]}}]	10	3
87	2025-10-31 22:45:00.420575+00	53	Love Machine - Arctic Monkeys	2	[{"changed": {"fields": ["Genre"]}}]	10	3
88	2025-10-31 22:45:07.906218+00	52	Sweater Weather - The Neighbourhood	2	[{"changed": {"fields": ["Genre"]}}]	10	3
89	2025-10-31 22:45:15.59647+00	50	Pretty Boy - The Neighbourhood	2	[{"changed": {"fields": ["Genre"]}}]	10	3
90	2025-10-31 22:45:23.890253+00	49	Sweater Weather (radio edit) - The Neighbourhood	2	[{"changed": {"fields": ["Genre"]}}]	10	3
91	2025-10-31 22:45:31.837275+00	48	Let It Go - The Neighbourhood	2	[{"changed": {"fields": ["Genre"]}}]	10	3
92	2025-10-31 22:45:45.522299+00	47	Big Long Line - The Neighbourhood	2	[{"changed": {"fields": ["Genre"]}}]	10	3
93	2025-10-31 22:46:14.110109+00	32	high school - Lil Peep	2	[{"changed": {"fields": ["Genre"]}}]	10	3
94	2025-10-31 22:46:28.044035+00	31	five degrees - Lil Peep	2	[{"changed": {"fields": ["Genre"]}}]	10	3
95	2025-10-31 22:46:32.262009+00	30	Keep My Coo - Lil Peep	2	[{"changed": {"fields": ["Genre"]}}]	10	3
96	2025-10-31 22:46:37.240246+00	29	broken smile (og version) - Lil Peep	2	[{"changed": {"fields": ["Genre"]}}]	10	3
97	2025-10-31 22:46:42.502949+00	28	Yah Mean - Playboi Carti	2	[{"changed": {"fields": ["Genre"]}}]	10	3
98	2025-10-31 22:47:00.264286+00	27	Location - Playboi Carti	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
99	2025-10-31 22:47:16.68013+00	26	Long Time (intro) - Playboi Carti	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
100	2025-10-31 22:47:36.579514+00	25	Kelly K - Playboi Carti	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
101	2025-10-31 22:47:54.822668+00	24	KETAMINE - Playboi Carti	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
102	2025-10-31 22:48:40.601674+00	23	Over - Playboi Carti	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
103	2025-10-31 22:48:55.566424+00	22	Sky - Playboi Carti	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
104	2025-10-31 22:49:06.444984+00	21	Control - Playboi Carti	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
105	2025-10-31 22:49:21.258009+00	20	Meh - Playboi Carti	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
106	2025-10-31 22:49:34.381054+00	19	JumpOutTheHouse - Playboi Carti	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
107	2025-10-31 22:49:44.807842+00	12	Shots (The Funk Hunters remix) - Imagine Dragons	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
108	2025-10-31 22:50:10.960602+00	10	Natural - Imagine Dragons	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
109	2025-10-31 22:51:33.16108+00	8	Twist & Shout BBC Session 30 juli 1963) - The Beatles	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
110	2025-10-31 22:52:05.325927+00	7	Hello Goodbye - The Beatles	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)", "Czas trwania"]}}]	10	3
111	2025-10-31 22:52:42.598484+00	6	Come Together - The Beatles	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)", "Czas trwania"]}}]	10	3
112	2025-10-31 22:53:12.724705+00	5	Hey Jude - The Beatles	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)", "Czas trwania"]}}]	10	3
113	2025-10-31 22:53:40.63336+00	4	The Girl I Love - The Beatles	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
114	2025-10-31 22:55:03.861809+00	46	That Way (instrumental) - The Neighbourhood	2	[{"changed": {"fields": ["Genre"]}}]	10	3
115	2025-10-31 22:55:17.179965+00	45	Missing Out - The Neighbourhood	2	[{"changed": {"fields": ["Genre"]}}]	10	3
116	2025-10-31 22:55:26.30681+00	44	A The Time (B the Inclination) - The Neighbourhood	2	[{"changed": {"fields": ["Genre"]}}]	10	3
117	2025-10-31 22:55:35.240053+00	43	No! - ThxSoMch	2	[{"changed": {"fields": ["Genre"]}}]	10	3
118	2025-10-31 22:55:44.763235+00	42	Bad Dream - ThxSoMch	2	[{"changed": {"fields": ["Genre"]}}]	10	3
119	2025-10-31 22:56:12.660277+00	41	CAROLINE - ThxSoMch	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
120	2025-10-31 22:56:49.238179+00	40	Knocking At My Door - ThxSoMch	2	[{"changed": {"fields": ["Genre", "Czas trwania"]}}]	10	3
121	2025-10-31 22:57:03.44654+00	39	Waste My Mind - ThxSoMch	2	[{"changed": {"fields": ["Genre"]}}]	10	3
122	2025-10-31 22:57:16.157001+00	38	Awfully Sad - ThxSoMch	2	[{"changed": {"fields": ["Genre"]}}]	10	3
123	2025-10-31 22:57:30.137242+00	37	I'll Love Who I'll Love - ThxSoMch	2	[{"changed": {"fields": ["Genre"]}}]	10	3
124	2025-10-31 22:57:37.206893+00	36	Aim For The Bushes - ThxSoMch	2	[{"changed": {"fields": ["Genre"]}}]	10	3
125	2025-10-31 22:57:44.478828+00	35	A Sharp Pain - ThxSoMch	2	[{"changed": {"fields": ["Genre"]}}]	10	3
126	2025-10-31 22:58:05.952705+00	34	Knocking at My Door - ThxSoMch	2	[{"changed": {"fields": ["Genre", "Data utworu (autora)"]}}]	10	3
127	2025-10-31 22:58:32.367566+00	3	Dark side of the moon - suisside	2	[{"changed": {"fields": ["Data utworu (autora)", "Czas trwania"]}}]	10	3
128	2025-10-31 22:59:19.921026+00	11	Next to Me - Imagine Dragons	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
129	2025-10-31 22:59:34.677485+00	13	Digital - Imagine Dragons	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
130	2025-10-31 22:59:49.845718+00	28	Yah Mean - Playboi Carti	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
131	2025-10-31 23:00:01.385792+00	14	Burn Out - Imagine Dragons	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
132	2025-10-31 23:00:13.966916+00	29	broken smile (og version) - Lil Peep	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
133	2025-10-31 23:00:25.396301+00	72	Utterance Beyond Death - Bones	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
134	2025-10-31 23:00:41.541438+00	71	Execration Rites - Bones	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
135	2025-10-31 23:00:53.339692+00	70	Deserts of Eternity - Bones	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
136	2025-10-31 23:01:21.394573+00	69	1000 Lies - Bones	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
137	2025-10-31 23:01:31.580947+00	53	Love Machine - Arctic Monkeys	2	[{"changed": {"fields": ["Data utworu (autora)"]}}]	10	3
138	2025-11-02 21:34:58.448143+00	3	admin	2	[{"changed": {"fields": ["Favorite genres", "Favorite artists", "Bio"]}}]	6	3
139	2025-11-17 23:56:07.596718+00	53	Experimental	1	[{"added": {}}]	11	3
140	2025-11-17 23:56:14.094576+00	54	Industrial	1	[{"added": {}}]	11	3
141	2025-11-17 23:56:17.96113+00	55	Noise	1	[{"added": {}}]	11	3
142	2025-11-18 13:29:40.280784+00	9	Sasha	3		6	3
143	2025-11-18 14:06:07.502517+00	11	Oleksandr	3		6	3
144	2025-11-18 14:17:17.808869+00	12	Oleksandr	3		6	3
145	2025-11-18 14:19:19.082225+00	13	Oleksandr	3		6	3
146	2025-11-19 23:25:17.104548+00	14	Oleksandr	3		6	3
147	2025-11-20 22:12:31.644049+00	15	Oleksandr	3		6	3
148	2025-12-10 23:58:10.723032+00	16	Oleksandr1	2	[{"changed": {"fields": ["Username"]}}]	6	3
149	2025-12-10 23:58:56.928102+00	6	test3	3		6	3
150	2026-01-07 13:46:07.682183+00	83	Love & Affection - ilyTOMMY	2	[{"changed": {"fields": ["Genre"]}}]	10	3
151	2026-01-07 13:46:13.897808+00	87	Life Is Pointless - ilyTOMMY	2	[{"changed": {"fields": ["Genre"]}}]	10	3
152	2026-01-07 13:46:24.084807+00	86	Forever - ilyTOMMY	2	[{"changed": {"fields": ["Genre"]}}]	10	3
153	2026-01-07 13:46:29.712964+00	85	Forever (Slowed Down) - ilyTOMMY	2	[{"changed": {"fields": ["Genre"]}}]	10	3
154	2026-01-07 13:46:38.214428+00	84	Marceline - ilyTOMMY	2	[{"changed": {"fields": ["Genre"]}}]	10	3
\.


ALTER TABLE public.django_admin_log ENABLE TRIGGER ALL;

--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.django_migrations DISABLE TRIGGER ALL;

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-10-01 19:12:29.728653+00
2	contenttypes	0002_remove_content_type_name	2025-10-01 19:12:29.735069+00
3	auth	0001_initial	2025-10-01 19:12:29.759684+00
4	auth	0002_alter_permission_name_max_length	2025-10-01 19:12:29.763688+00
5	auth	0003_alter_user_email_max_length	2025-10-01 19:12:29.76569+00
6	auth	0004_alter_user_username_opts	2025-10-01 19:12:29.768693+00
7	auth	0005_alter_user_last_login_null	2025-10-01 19:12:29.771988+00
8	auth	0006_require_contenttypes_0002	2025-10-01 19:12:29.771988+00
9	auth	0007_alter_validators_add_error_messages	2025-10-01 19:12:29.775992+00
10	auth	0008_alter_user_username_max_length	2025-10-01 19:12:29.777994+00
11	auth	0009_alter_user_last_name_max_length	2025-10-01 19:12:29.780997+00
12	auth	0010_alter_group_name_max_length	2025-10-01 19:12:29.785576+00
13	auth	0011_update_proxy_permissions	2025-10-01 19:12:29.78858+00
14	auth	0012_alter_user_first_name_max_length	2025-10-01 19:12:29.790581+00
15	users	0001_initial	2025-10-01 19:12:29.813602+00
16	admin	0001_initial	2025-10-01 19:12:29.825613+00
17	admin	0002_logentry_remove_auto_add	2025-10-01 19:12:29.829617+00
18	admin	0003_logentry_add_action_flag_choices	2025-10-01 19:12:29.83262+00
19	authtoken	0001_initial	2025-10-01 19:12:29.841627+00
20	authtoken	0002_auto_20160226_1747	2025-10-01 19:12:29.85464+00
21	authtoken	0003_tokenproxy	2025-10-01 19:12:29.855249+00
22	authtoken	0004_alter_tokenproxy_options	2025-10-01 19:12:29.858253+00
23	sessions	0001_initial	2025-10-01 19:12:29.864257+00
24	music	0001_initial	2025-10-01 20:23:55.38883+00
25	users	0002_alter_user_options_alter_user_bio_alter_user_email_and_more	2025-10-21 22:11:49.166997+00
26	music	0002_review	2025-10-29 12:28:09.29825+00
27	music	0003_alter_track_options_alter_review_unique_together_and_more	2025-10-29 12:32:23.292801+00
28	music	0004_track_average_rating_cached_and_more	2025-10-29 14:42:24.461069+00
29	music	0005_remove_review_rating_between_1_and_5_and_more	2025-10-29 20:04:09.474384+00
30	music	0006_review_title	2025-10-30 23:47:29.649805+00
31	music	0007_reviewlike	2025-10-31 00:58:07.481112+00
32	music	0008_track_authored_date_track_duration	2025-10-31 12:32:20.809623+00
33	music	0009_track_cover_image	2025-10-31 14:35:11.385145+00
34	users	0003_user_xp	2025-11-01 23:39:53.457204+00
35	music	0010_favorite	2025-11-05 23:57:02.469851+00
36	users	0004_alter_user_xp_user_users_user_xp_check	2025-11-06 14:31:34.152565+00
37	users	0005_remove_user_users_user_xp_check	2025-11-06 14:31:34.164164+00
38	users	0006_user_profile_picture	2025-11-07 20:05:25.014581+00
39	music	0011_playlist_playlisttrack_playlist_tracks_and_more	2025-11-08 02:52:30.571675+00
40	users	0007_userblock_userfollow	2025-11-08 15:52:25.552845+00
41	music	0012_playlist_is_public	2025-11-08 18:57:32.369071+00
42	users	0008_user_email_verification_sent_at_and_more	2025-11-10 00:10:46.021595+00
43	users	0009_errorreport	2025-11-10 19:40:58.054095+00
44	users	0010_errorreport_content_id_errorreport_content_type_and_more	2025-11-10 23:31:14.202758+00
45	chat	0001_initial	2025-11-11 13:17:23.68868+00
46	groups	0001_initial	2025-11-11 22:10:01.650883+00
47	chat	0002_groupchatmessage_groupchatread	2025-11-12 16:43:51.947181+00
48	users	0011_user_city	2025-11-12 23:52:29.249561+00
49	events	0001_initial	2025-11-14 12:57:47.637013+00
50	events	0002_event_end_date_alter_event_event_date_and_more	2025-11-14 15:12:18.466991+00
51	events	0003_eventrating	2025-11-16 14:12:04.891743+00
52	events	0004_eventpoll_pollvote	2025-11-16 16:25:24.685958+00
53	events	0005_event_playlist	2025-11-17 14:12:20.214941+00
54	music	0013_playlist_is_event_playlist_alter_track_cover_image	2025-11-20 15:47:38.059252+00
\.


ALTER TABLE public.django_migrations ENABLE TRIGGER ALL;

--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.django_session DISABLE TRIGGER ALL;

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
vpenimjbae6hdbl6ldl208s39zrprpkg	.eJxVjDsOwjAQBe_iGlna-MdS0nMGa9dr4wBypDipEHcnkVJA-2bmvVWkdalx7XmOo6iLMur0uzGlZ247kAe1-6TT1JZ5ZL0r-qBd3ybJr-vh_h1U6nWrgWzIIQGgRwsoDkIGPxhKzPZsrQtZgiEu4qkgFscIyW8VBzMgefX5AtJ7N7A:1vP646:XvXMVMIvZryRDkOIWEYe3OT6ji-HN-2fLjmGUQ8tmM0	2025-12-12 21:31:42.595915+00
9lvj59sxqsk1r7s55hn3y925evmkzz5h	.eJxVjMEOwiAQBf-FsyFlCwF69O43kAW2ghowpU00xn9Xkh70-mbevJjDbU1ua7S4HNnEgB1-N4_hSqWDeMFyrjzUsi7Z867wnTZ-qpFux939CyRs6fsORhlEabUBTz6CHgN5JAHCBmOFlDAHQg0SB8JxptlCNEppRQoFyaFHG7WWa3H0uOflyabh_QGtIj-h:1vBZXi:mGRuy2CQB0CA4GygxFv0kuc8FfNvh8UXtXj2_Rtuncw	2025-11-05 14:10:22.664442+00
hulc1y3oz8ghql5j0hdtmv0i9a48kgtl	.eJxVjMEOwiAQBf-FsyFlCwF69O43kAW2ghowpU00xn9Xkh70-mbevJjDbU1ua7S4HNnEgB1-N4_hSqWDeMFyrjzUsi7Z867wnTZ-qpFux939CyRs6fsORhlEabUBTz6CHgN5JAHCBmOFlDAHQg0SB8JxptlCNEppRQoFyaFHG7WWa3H0uOflyabh_QGtIj-h:1vBZZ3:SAB_De_tLq1VmXvxF_qntQDZOFTe1Cb4FpCOONm8NxM	2025-11-05 14:11:45.104958+00
rm6kque1t6kltf19nvuctrmc5tcrarvv	.eJxVjDsOwjAQBe_iGlna-MdS0nMGa9dr4wBypDipEHcnkVJA-2bmvVWkdalx7XmOo6iLMur0uzGlZ247kAe1-6TT1JZ5ZL0r-qBd3ybJr-vh_h1U6nWrgWzIIQGgRwsoDkIGPxhKzPZsrQtZgiEu4qkgFscIyW8VBzMgefX5AtJ7N7A:1vWOlc:iPVC3ODOZymZCkjkg8pfXW0gIKYtuLS3YkjKwMZA57Q	2026-01-02 00:54:48.773844+00
quxatb3hp1zoidig0vy1rg650croaj1t	.eJxVjMEOwiAQBf-FsyFlCwF69O43kAW2ghowpU00xn9Xkh70-mbevJjDbU1ua7S4HNnEgB1-N4_hSqWDeMFyrjzUsi7Z867wnTZ-qpFux939CyRs6fsORhlEabUBTz6CHgN5JAHCBmOFlDAHQg0SB8JxptlCNEppRQoFyaFHG7WWa3H0uOflyabh_QGtIj-h:1vBrnZ:Y6Aj4B9wmyCL8Ik5hRAZYMfzvP475hf2Lkxn3juCyVI	2025-11-06 09:39:57.817363+00
1p485ew3m947r7zawk90f0a3tdowqmsl	.eJxVjEEOwiAURO_C2hDgA6Uu3fcMBPgfqRpISrsy3t026UJ3k3lv5s182Nbit06Ln5FdmWGX3y6G9KR6AHyEem88tbouc-SHwk_a-dSQXrfT_TsooZd9DcIYTBltJuPUnozGAWgYrRBRZVBuDMkZqYULBCStkFmTBSXQqZyAfb7oLjem:1vaFBW:T87dwuc7gtae1JHEyLQ_fXeORMosN01Ln4XYYIa2ZLs	2026-01-12 15:29:26.097921+00
bktmes5fmqhhqhw2o0di993x2pik5vfm	.eJxVjDsOwjAQBe_iGlna-MdS0nMGa9dr4wBypDipEHcnkVJA-2bmvVWkdalx7XmOo6iLMur0uzGlZ247kAe1-6TT1JZ5ZL0r-qBd3ybJr-vh_h1U6nWrgWzIIQGgRwsoDkIGPxhKzPZsrQtZgiEu4qkgFscIyW8VBzMgefX5AtJ7N7A:1vdFfp:E_5AdXRbNwPaxNRqXc4B3Ub26Wlg3mhT4QK_NQTg-_Q	2026-01-20 22:37:09.143824+00
3otwdr4bwg40hhsdkyhmboe1tpi0w323	.eJxVjEEOwiAURO_C2hDgA6Uu3fcMBPgfqRpISrsy3t026UJ3k3lv5s182Nbit06Ln5FdmWGX3y6G9KR6AHyEem88tbouc-SHwk_a-dSQXrfT_TsooZd9DcIYTBltJuPUnozGAWgYrRBRZVBuDMkZqYULBCStkFmTBSXQqZyAfb7oLjem:1vfqLf:FmX0TQO5rtJSCWvFmeQjpZTyer-TLScXas-QazH1xkE	2026-01-28 02:11:03.289043+00
\.


ALTER TABLE public.django_session ENABLE TRIGGER ALL;

--
-- Data for Name: music_playlist; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.music_playlist DISABLE TRIGGER ALL;

COPY public.music_playlist (id, name, description, cover_image, is_favorite, created_at, updated_at, user_id, is_public, is_event_playlist) FROM stdin;
2	Ulubione	Twoje ulubione utwory		t	2025-11-08 03:17:34.687897+00	2025-11-08 03:17:34.687897+00	3	f	f
9	My playlist			f	2025-11-18 13:52:52.061577+00	2025-11-18 13:52:52.061577+00	2	t	f
13	Techno Marathon: 12h Non-Stop	Playlista wydarzenia: Techno Marathon: 12h Non-Stop		f	2025-11-19 23:41:19.634391+00	2025-11-19 23:41:19.634391+00	2	t	f
14	2222	Playlista wydarzenia: 2222		f	2025-11-20 15:49:57.391846+00	2025-11-20 15:49:57.391846+00	3	t	t
15	222	Playlista wydarzenia: 222		f	2025-11-20 19:16:19.828942+00	2025-11-20 19:16:19.828942+00	2	t	t
16	First playlist		playlist_covers/6666.jfif	f	2025-11-20 22:17:08.99003+00	2025-11-20 22:17:08.993005+00	16	t	f
17	Ulubione	Twoje ulubione utwory		t	2025-11-20 22:17:26.71384+00	2025-11-20 22:17:26.71384+00	16	f	f
18	Modular Synthesis Workshop	Playlista wydarzenia: Modular Synthesis Workshop		f	2025-11-20 22:23:55.948175+00	2025-11-20 22:23:55.948175+00	16	t	t
19	213	Playlista wydarzenia: 213		f	2025-11-22 00:15:32.938378+00	2025-11-22 00:15:32.938378+00	3	t	t
20	1111	Playlista wydarzenia: 1111		f	2025-11-28 23:27:19.493216+00	2025-11-28 23:27:19.493216+00	16	t	t
23	2222	Playlista wydarzenia: 2222		f	2025-12-22 19:53:27.366129+00	2025-12-22 19:53:27.366129+00	3	t	t
24	Ulubione	Twoje ulubione utwory		t	2025-12-22 22:49:03.184654+00	2025-12-22 22:49:03.184654+00	2	f	f
25	Ulubione	Twoje ulubione utwory		t	2025-12-29 15:29:35.049928+00	2025-12-29 15:29:35.049928+00	5	f	f
26	Test1	Playlista wydarzenia: Test1		f	2026-01-06 15:10:52.23647+00	2026-01-06 15:10:52.23647+00	3	t	t
12	Late Night Jazz Session	Playlista wydarzenia: Late Night Jazz Session	playlist_covers/11.jfif	f	2025-11-19 23:29:55.765168+00	2026-01-06 21:27:43.982693+00	3	t	f
5	Underground Cypher	Playlista wydarzenia: Underground Cypher	playlist_covers/9999.jfif	f	2025-11-18 00:08:45.398292+00	2026-01-06 21:28:00.402727+00	3	t	f
6	ThxSoMuch	Playlista wydarzenia: ThxSoMuch	playlist_covers/4444.jfif	f	2025-11-18 13:14:56.565789+00	2026-01-06 21:28:18.826955+00	3	t	f
1	Moja Playlista		playlist_covers/playlist.jfif	f	2025-11-08 03:10:56.456525+00	2026-01-06 23:31:52.549509+00	3	t	f
27	sad	Playlista wydarzenia: sad		f	2026-01-14 02:21:27.961899+00	2026-01-14 02:21:27.961899+00	3	t	t
\.


ALTER TABLE public.music_playlist ENABLE TRIGGER ALL;

--
-- Data for Name: events_event; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.events_event DISABLE TRIGGER ALL;

COPY public.events_event (id, title, slug, description, location, event_date, event_image, created_at, updated_at, creator_id, group_id, end_date, playlist_id) FROM stdin;
21	Test1	test1	test1	Club XYZ, ul. Główna 123, Warszawa	2026-01-07 15:10:00+00	event_images/Spike_Spiegel.jfif	2026-01-06 15:10:52.242252+00	2026-01-06 23:36:35.628165+00	3	9	2026-01-09 15:10:00+00	26
22	sad	sad	asd	Club XYZ, ul. Główna 123, Warszawa	2026-01-16 02:21:00+00		2026-01-14 02:21:27.968854+00	2026-01-14 02:21:27.968854+00	3	9	2026-01-23 02:21:00+00	27
2	Koncert	koncert	123123412412442124	Club XYZ, ul. Główna 123	2025-11-14 16:29:00+00	event_images/events_I6Ugo5o.jfif	2025-11-14 15:27:57.67492+00	2025-11-14 15:40:47.091363+00	3	1	2025-11-14 16:36:00+00	\N
6	ZXCursed	zxcursed	Fun	Zlote Tarasy	2025-11-16 15:55:00+00	event_images/7777.jfif	2025-11-16 15:54:39.296227+00	2025-11-17 15:36:40.585628+00	3	1	2025-11-16 15:56:00+00	\N
11	Underground Cypher	underground-cypher	Comiesięczny cypher dla rapperów i bitmakerów. Otwarta scena, freestyle battles i networking. Bring your best bars!	Klub Hydrozagadka, ul. Bracka 20	2025-11-25 19:00:00+00	event_images/111.jfif	2025-11-18 00:08:45.403296+00	2025-11-18 00:08:45.403296+00	3	3	2025-11-26 01:00:00+00	5
12	ThxSoMuch	thxsomuch	Miejsce dla prawdziwych fanów tego wykonawcy, gdzie razem możemy cieszyć się wszystkimi jego utworami 	Klub Hybrydy	2025-11-28 15:14:00+00	event_images/4444.jfif	2025-11-18 13:14:56.571794+00	2025-11-18 13:19:44.52789+00	3	9	2025-11-28 19:20:00+00	6
7	IVOXYGEN	ivoxygen	For all rock funs	Stare miasto	2025-11-16 17:39:00+00	event_images/9999.jfif	2025-11-16 16:40:29.909509+00	2025-11-18 13:21:59.601962+00	3	1	2025-11-16 17:09:00+00	\N
13	Late Night Jazz Session	late-night-jazz-session	Wieczór z żywym jazzem. Gościnnie wystąpi trio Jana Ptaszyna Wróblewskiego. Jam session po koncercie.	Harris Piano Jazz Bar, Rynek Główny 28	2025-11-28 19:33:00+00	event_images/5555.jfif	2025-11-19 23:29:55.770021+00	2025-11-19 23:29:55.770021+00	3	4	2025-11-28 22:30:00+00	12
14	Techno Marathon: 12h Non-Stop	techno-marathon-12h-non-stop	Całonocny maraton techno. 6 DJs, raw sound system i industrialne wnętrza. Tylko dla hardkorowych ravers.	Magazyn Warehouse, ul. Przemysłowa 15	2025-11-25 09:40:00+00	event_images/2222.jfif	2025-11-19 23:41:19.639548+00	2025-11-19 23:41:19.639548+00	2	5	2025-11-25 22:40:00+00	13
10	222	222-1	2222	2222	2025-11-17 18:23:00+00	event_images/8888.jfif	2025-11-17 14:26:46.456002+00	2025-11-17 15:35:27.61726+00	3	1	2025-11-17 20:23:00+00	\N
15	2222	2222	2222	2222	2025-11-22 15:49:00+00	event_images/6666_zVjDzwN.jfif	2025-11-20 15:49:57.396851+00	2025-11-20 15:49:57.396851+00	3	1	2025-11-22 18:49:00+00	14
17	Modular Synthesis Workshop	modular-synthesis-workshop	Warsztat z syntezatorów modularowych. Nauczysz się podstaw patchingu i stworzysz własne soundy. Sprzęt zapewniony!	Strefa Kultury, ul. Rakowicka 10A	2025-11-27 02:28:00+00	event_images/Без_названия.jfif	2025-11-20 22:23:55.952178+00	2025-11-20 22:23:55.952178+00	16	11	2025-11-27 09:29:00+00	18
18	213	213	12	123123	2025-11-23 00:15:00+00	event_images/Без_названия_PALXorz.jfif	2025-11-22 00:15:32.944501+00	2025-11-22 00:15:32.944501+00	3	5	2025-11-24 00:15:00+00	19
19	1111	1111	111111	1111	2025-12-03 23:26:00+00	event_images/Drawn_by_a_mouse__DD.jfif	2025-11-28 23:27:19.499221+00	2025-11-28 23:27:19.499221+00	16	9	2025-12-04 11:32:00+00	20
\.


ALTER TABLE public.events_event ENABLE TRIGGER ALL;

--
-- Data for Name: events_eventattendee; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.events_eventattendee DISABLE TRIGGER ALL;

COPY public.events_eventattendee (id, status, created_at, event_id, user_id) FROM stdin;
4	going	2025-11-14 15:27:57.676923+00	2	3
5	going	2025-11-14 15:35:32.14666+00	2	2
9	going	2025-11-16 15:54:39.298228+00	6	3
11	going	2025-11-16 15:55:53.351349+00	6	2
12	going	2025-11-16 16:40:29.910511+00	7	3
17	going	2025-11-17 14:26:46.457002+00	10	3
20	going	2025-11-17 17:10:14.883517+00	10	2
22	going	2025-11-18 00:08:45.405297+00	11	3
23	going	2025-11-18 13:14:56.573796+00	12	3
26	going	2025-11-19 23:29:55.772023+00	13	3
33	going	2025-11-19 23:58:11.858427+00	14	3
34	going	2025-11-19 23:58:22.137351+00	14	2
36	going	2025-11-20 15:49:57.397852+00	15	3
39	going	2025-11-20 22:20:50.932485+00	14	16
40	going	2025-11-20 22:23:55.954296+00	17	16
41	going	2025-11-20 22:24:49.122837+00	11	16
42	going	2025-11-22 00:15:32.946503+00	18	3
47	going	2026-01-06 15:11:12.507891+00	21	3
51	going	2026-01-14 02:21:27.970502+00	22	3
\.


ALTER TABLE public.events_eventattendee ENABLE TRIGGER ALL;

--
-- Data for Name: events_eventpoll; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.events_eventpoll DISABLE TRIGGER ALL;

COPY public.events_eventpoll (id, poll_type, title, description, proposed_date, proposed_end_date, proposed_location, is_active, created_at, closes_at, creator_id, event_id) FROM stdin;
1	time	Zmiana czasu	Bo mi nie pasuje	2025-11-16 17:44:00+00	2025-11-16 18:45:00+00		t	2025-11-16 16:42:12.527534+00	2025-11-16 16:45:00+00	3	7
2	other	asdasda	asdasdasd	\N	\N		f	2025-11-16 16:58:37.319979+00	2025-11-16 17:00:00+00	3	7
3	other	sadasdasd	asdasdasd	\N	\N		t	2025-11-16 16:59:14.569651+00	2025-11-16 17:00:00+00	3	7
8	location	Inne miejsce	Stare miejsce juz zajete 	\N	\N	Zlota 44	t	2025-11-19 23:46:48.004921+00	2025-11-19 23:48:00+00	2	14
9	other	213	2131	\N	\N		t	2025-11-19 23:52:02.042074+00	2025-11-19 23:53:00+00	2	14
10	other	213123	123123123	\N	\N		f	2025-11-20 00:04:23.564983+00	2025-11-20 00:06:00+00	3	14
13	other	New changes	change playlist	\N	\N		t	2025-11-20 22:21:38.286025+00	2025-11-20 22:23:00+00	16	14
14	time	asdasd	dsadsadsa	2026-01-16 15:27:00+00	2026-01-08 15:27:00+00		t	2026-01-06 15:27:30.208024+00	2026-01-09 15:27:00+00	3	21
\.


ALTER TABLE public.events_eventpoll ENABLE TRIGGER ALL;

--
-- Data for Name: events_eventrating; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.events_eventrating DISABLE TRIGGER ALL;

COPY public.events_eventrating (id, rating, comment, created_at, event_id, user_id) FROM stdin;
2	4	asdasd	2025-11-16 15:52:23.009069+00	2	2
4	5	zxc	2025-11-18 12:54:55.299049+00	6	3
5	5	adsad	2025-11-21 18:10:24.754466+00	10	3
11	4	dsf	2025-12-22 19:50:47.992121+00	2	3
\.


ALTER TABLE public.events_eventrating ENABLE TRIGGER ALL;

--
-- Data for Name: events_pollvote; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.events_pollvote DISABLE TRIGGER ALL;

COPY public.events_pollvote (id, vote, created_at, poll_id, user_id) FROM stdin;
1	t	2025-11-16 16:42:28.374171+00	1	3
2	t	2025-11-16 16:43:50.408885+00	1	2
3	t	2025-11-16 16:58:43.952907+00	2	3
4	t	2025-11-16 16:59:16.421401+00	3	3
10	t	2025-11-19 23:46:52.004147+00	8	2
11	f	2025-11-19 23:52:03.872199+00	9	2
12	t	2025-11-20 00:04:32.512704+00	10	2
16	t	2025-11-20 22:21:41.715993+00	13	16
\.


ALTER TABLE public.events_pollvote ENABLE TRIGGER ALL;

--
-- Data for Name: music_genre; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.music_genre DISABLE TRIGGER ALL;

COPY public.music_genre (id, name) FROM stdin;
1	Rock
2	hip-hop
3	emo rap
4	Indie rock
5	Trance
6	Electronic
7	Unknown
8	Pop
9	Rap
10	R&B
11	Soul
12	Jazz
13	Blues
14	Classical
15	EDM
16	House
17	Techno
18	Dubstep
19	Drum & Bass
20	Reggae
21	Dancehall
22	Afrobeat
23	Latin
24	Reggaeton
25	Country
26	Folk
27	Indie
28	Alternative
29	Metal
30	Heavy Metal
31	Punk
32	Emo
33	Funk
34	Disco
35	K-pop
36	J-pop
37	C-pop
38	Lo-fi
39	Ambient
40	Soundtrack / Score
41	Gospel
42	Opera
43	Dance-Pop
44	Trap
45	Drill
46	Ska
47	Synth-pop
48	New Wave
49	Grunge
50	Soft Rock
51	Hard Rock
52	World Music
53	Experimental
54	Industrial
55	Noise
\.


ALTER TABLE public.music_genre ENABLE TRIGGER ALL;

--
-- Data for Name: groups_group_genres; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.groups_group_genres DISABLE TRIGGER ALL;

COPY public.groups_group_genres (id, group_id, genre_id) FROM stdin;
1	1	18
2	1	11
3	1	21
4	1	14
8	3	9
9	3	2
10	4	12
11	4	13
12	5	16
13	5	17
14	5	6
15	6	1
16	6	28
17	6	31
18	7	18
19	7	20
20	7	46
21	8	53
22	8	54
23	8	55
24	9	8
25	9	1
26	9	4
27	10	2
28	10	6
29	11	6
30	11	39
\.


ALTER TABLE public.groups_group_genres ENABLE TRIGGER ALL;

--
-- Data for Name: groups_groupinvitation; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.groups_groupinvitation DISABLE TRIGGER ALL;

COPY public.groups_groupinvitation (id, created_at, accepted, group_id, invited_by_id, invited_user_id) FROM stdin;
\.


ALTER TABLE public.groups_groupinvitation ENABLE TRIGGER ALL;

--
-- Data for Name: groups_groupmembership; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.groups_groupmembership DISABLE TRIGGER ALL;

COPY public.groups_groupmembership (id, status, joined_at, updated_at, group_id, user_id) FROM stdin;
1	accepted	2025-11-11 22:28:08.264507+00	2025-11-11 22:28:08.264507+00	1	3
11	accepted	2025-11-17 23:43:38.958485+00	2025-11-17 23:43:38.958485+00	3	3
12	accepted	2025-11-17 23:52:20.313848+00	2025-11-17 23:52:20.313848+00	4	3
13	accepted	2025-11-17 23:53:05.953076+00	2025-11-17 23:53:05.953076+00	5	3
14	accepted	2025-11-17 23:53:57.538309+00	2025-11-17 23:53:57.538309+00	6	3
15	accepted	2025-11-17 23:54:49.524265+00	2025-11-17 23:54:49.524265+00	7	3
16	accepted	2025-11-17 23:56:53.210457+00	2025-11-17 23:56:53.210457+00	8	3
17	accepted	2025-11-17 23:59:17.576451+00	2025-11-17 23:59:17.576451+00	9	3
18	accepted	2025-11-18 00:05:28.212509+00	2025-11-18 00:05:40.505948+00	1	2
23	accepted	2025-11-19 23:35:25.990868+00	2025-11-19 23:35:25.990868+00	5	2
24	accepted	2025-11-20 19:10:35.876721+00	2025-11-20 19:10:35.876721+00	10	2
25	accepted	2025-11-20 19:10:52.373307+00	2025-11-20 19:10:52.373307+00	10	3
28	accepted	2025-11-20 22:22:38.104178+00	2025-11-20 22:22:38.104178+00	11	16
30	accepted	2025-11-20 22:24:45.723463+00	2025-11-20 22:24:45.723463+00	3	16
31	accepted	2025-11-20 22:25:39.90149+00	2025-11-20 22:25:39.90149+00	11	3
29	accepted	2025-11-20 22:24:39.126341+00	2025-11-21 23:42:25.113119+00	9	16
26	accepted	2025-11-20 22:20:26.301348+00	2025-11-23 15:14:58.037503+00	1	16
34	accepted	2025-11-24 13:52:23.91171+00	2025-11-24 13:55:38.219414+00	4	2
33	accepted	2025-11-24 13:43:17.63874+00	2025-12-22 17:21:39.481923+00	9	2
36	accepted	2026-01-07 12:37:27.769256+00	2026-01-07 12:37:36.570909+00	9	5
37	accepted	2026-01-07 15:37:00.994672+00	2026-01-07 15:37:05.516631+00	1	5
38	accepted	2026-01-14 02:13:54.190459+00	2026-01-14 02:13:54.190459+00	4	5
\.


ALTER TABLE public.groups_groupmembership ENABLE TRIGGER ALL;

--
-- Data for Name: music_artist; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.music_artist DISABLE TRIGGER ALL;

COPY public.music_artist (id, name, bio) FROM stdin;
1	Drevo	Drevo music
2	IVOXYGEN	
3	suisside	
4	The Beatles	\N
5	Imagine Dragons	\N
6	Playboi Carti	\N
7	Lil Peep	\N
8	ThxSoMch	\N
9	The Neighbourhood	\N
10	Arctic Monkeys	\N
11	Bones	\N
12	BONES UK	\N
13	Face Face	\N
14	ilyTOMMY	\N
\.


ALTER TABLE public.music_artist ENABLE TRIGGER ALL;

--
-- Data for Name: music_track; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.music_track DISABLE TRIGGER ALL;

COPY public.music_track (id, title, description, created_at, artist_id, created_by_id, genre_id, average_rating_cached, reviews_count_cached, authored_date, duration, cover_image) FROM stdin;
29	broken smile (og version)	Zaimportowano z MusicBrainz (ID: 7821f7ea-16ef-4cf6-8478-ec777d64904c)	2025-10-31 21:03:37.891017+00	7	\N	25	\N	0	2017-05-22	00:02:41	http://coverartarchive.org/release/e4a4b907-3995-4b51-b549-fb7773c02edd/37200507497-250.jpg
3	Dark side of the moon		2025-10-29 23:07:29.414068+00	3	3	3	11.666666666666666	1	2025-04-07	00:01:56	\N
11	Next to Me	Імпортовано з MusicBrainz (ID: 23630a62-a74c-4efe-9bc0-8c844b41a811)	2025-10-31 14:42:14.245647+00	5	\N	4	\N	0	2020-06-19	00:03:50.288	http://coverartarchive.org/release/fb5be15f-1bbe-4275-aa0c-5d1cea590b14/25577981855-250.jpg
33	nothing to u	Zaimportowano z MusicBrainz (ID: 931d6b00-4186-454f-a84b-6587656143a8)	2025-10-31 21:03:49.631208+00	7	\N	3	\N	0	2024-09-18	00:02:27.692	https://coverartarchive.org/release/68c3e5eb-812b-42ec-926f-7a707a9445d2/39997640351-250.jpg
18	Tiptoe	Імпортовано з MusicBrainz (ID: e8e2d45d-0067-4b9e-a007-da79824dc3d8)	2025-10-31 14:42:34.075349+00	5	\N	1	\N	0	2023-12-13	00:03:14.2	https://coverartarchive.org/release/c417d74b-f610-432f-a1f1-54583ced6205/40887723467-250.jpg
17	Amsterdam	Імпортовано з MusicBrainz (ID: 2b50d4ec-9af7-49a4-8ad1-a5bbcd0b7437)	2025-10-31 14:42:31.902338+00	5	\N	1	\N	0	2022-11-10	00:04:10.493	https://coverartarchive.org/release/2d67b043-6266-4b83-87e7-c8a9258949bd/41986314903-250.jpg
16	Cha‐Ching (Till We Grow Older)	Імпортовано з MusicBrainz (ID: 54adc6e3-5d7f-4808-bdb6-ab7f3bf154ca)	2025-10-31 14:42:28.516363+00	5	\N	1	\N	0	2024-03-14	00:04:09.466	https://coverartarchive.org/release/b1bab550-32ce-4e14-9c3b-d13cb300021f/40887148361-250.jpg
15	Monster	Імпортовано з MusicBrainz (ID: b993af11-6b61-4e9a-9c3b-d5835c9cadc5)	2025-10-31 14:42:26.44393+00	5	\N	1	\N	0	2020-05-05	00:04:09.493	\N
9	My Fault	Імпортовано з MusicBrainz (ID: 078bb30b-5209-4523-8217-249726764717)	2025-10-31 14:42:12.178849+00	5	\N	1	\N	0	2019-07-09	00:02:56.253	https://coverartarchive.org/release/c417d74b-f610-432f-a1f1-54583ced6205/40887723467-250.jpg
1	Smaragdove Nebo	Top 10 songs of the week	2025-10-17 21:01:57.798642+00	1	3	1	78.33333333333333	1	2025-02-02	00:02:11	\N
32	high school	Zaimportowano z MusicBrainz (ID: 2e88633e-1de8-45e1-bb3d-c063715e8c67)	2025-10-31 21:03:46.837272+00	7	\N	32	\N	0	2024-09-18	00:02:48.071	https://coverartarchive.org/release/68c3e5eb-812b-42ec-926f-7a707a9445d2/39997640351-250.jpg
31	five degrees	Zaimportowano z MusicBrainz (ID: 23fec8a9-c4d1-4530-bad1-80b1faa2fa9a)	2025-10-31 21:03:44.119734+00	7	\N	39	\N	0	2024-09-18	00:02:24.103	https://coverartarchive.org/release/68c3e5eb-812b-42ec-926f-7a707a9445d2/39997640351-250.jpg
27	Location	Імпортовано з MusicBrainz (ID: 911f8aac-b5d0-4e58-bc04-217cead684c5)	2025-10-31 14:44:33.954817+00	6	\N	33	\N	0	2025-01-07	00:02:49	http://coverartarchive.org/release/eb08ad6b-c6d5-47be-81fc-959fb02f387c/37514136270-250.jpg
25	Kelly K	Імпортовано з MusicBrainz (ID: 61957666-58d0-4fe1-881e-b57deea71788)	2025-10-31 14:44:28.199767+00	6	\N	30	\N	0	2024-07-15	00:04:31	http://coverartarchive.org/release/eb08ad6b-c6d5-47be-81fc-959fb02f387c/37514136270-250.jpg
24	KETAMINE	Імпортовано з MusicBrainz (ID: 79ee9383-b406-4d0f-8b09-800fb988a2c0)	2025-10-31 14:44:25.46171+00	6	\N	6	\N	0	2023-10-16	00:01:54	https://coverartarchive.org/release/a737ad9a-b171-427c-969e-60894eb22b33/38387940472-250.jpg
23	Over	Імпортовано з MusicBrainz (ID: aa83c746-b959-4631-848f-90eeca7a0fad)	2025-10-31 14:44:22.615822+00	6	\N	34	\N	0	2025-05-07	00:02:46	https://coverartarchive.org/release/08b4c6b5-651b-4612-bf75-e8345a263802/37188298947-250.jpg
22	Sky	Імпортовано з MusicBrainz (ID: e725a6a4-e390-4836-8eff-4b27a800a52d)	2025-10-31 14:44:20.126559+00	6	\N	21	\N	0	2024-10-31	00:03:13	https://coverartarchive.org/release/08b4c6b5-651b-4612-bf75-e8345a263802/37188298947-250.jpg
21	Control	Імпортовано з MusicBrainz (ID: 69707cf4-39b5-4c11-8344-c355d7921783)	2025-10-31 14:44:18.182654+00	6	\N	48	\N	0	2025-07-13	00:03:18	https://coverartarchive.org/release/08b4c6b5-651b-4612-bf75-e8345a263802/37188298947-250.jpg
20	Meh	Імпортовано з MusicBrainz (ID: f075ef0d-94c0-4e5b-9761-70c49cd5af24)	2025-10-31 14:44:15.710186+00	6	\N	10	\N	0	2025-08-06	00:01:59	https://coverartarchive.org/release/08b4c6b5-651b-4612-bf75-e8345a263802/37188298947-250.jpg
19	JumpOutTheHouse	Імпортовано з MusicBrainz (ID: 8732214c-a20c-42cc-b72f-b99c663d2c70)	2025-10-31 14:44:13.730262+00	6	\N	8	\N	0	2025-01-25	00:01:33	https://coverartarchive.org/release/08b4c6b5-651b-4612-bf75-e8345a263802/37188298947-250.jpg
12	Shots (The Funk Hunters remix)	Імпортовано з MusicBrainz (ID: 93f10a93-caaa-4da6-ac51-a94ad2ab109a)	2025-10-31 14:42:19.461881+00	5	\N	24	\N	0	2025-07-03	00:04:45.976	https://coverartarchive.org/release/6a909a7f-193f-4fda-8596-be0e38daf90c/41253082947-250.jpg
10	Natural	Імпортовано з MusicBrainz (ID: 7347472e-a25b-4c4a-8317-f5f9c5e998d1)	2025-10-31 14:42:12.181851+00	5	\N	44	\N	0	2021-04-05	00:03:09	\N
8	Twist & Shout BBC Session 30 juli 1963)	Імпортовано з MusicBrainz (ID: 2b31c038-4b7c-44ad-b6f2-d84ccaba1a3f)	2025-10-31 13:36:42.53668+00	4	\N	23	\N	0	2015-06-22	00:02:28.126	\N
7	Hello Goodbye	Імпортовано з MusicBrainz (ID: e8492e62-175f-4d31-9815-d5af4d767ff2)	2025-10-31 13:36:42.534679+00	4	\N	26	\N	0	2012-10-06	00:02:44	\N
6	Come Together	Імпортовано з MusicBrainz (ID: 4181ff9d-401e-4914-b72c-fa0390b32278)	2025-10-31 13:36:42.532677+00	4	\N	47	\N	0	2005-04-06	00:03:02	\N
5	Hey Jude	Імпортовано з MusicBrainz (ID: 1965c130-06c3-4df9-a662-b1901fc4c926)	2025-10-31 13:36:42.531676+00	4	\N	34	\N	0	2007-03-06	00:03:32	\N
4	The Girl I Love	Імпортовано з MusicBrainz (ID: 252224e9-f0ce-4cd9-826c-49ab21c4dedb)	2025-10-31 13:36:42.528673+00	4	\N	1	\N	0	2004-02-18	00:02:09	\N
13	Digital	Імпортовано з MusicBrainz (ID: 5d6d204e-98fa-4512-9d0c-c74e6c6c3730)	2025-10-31 14:42:22.305367+00	5	\N	5	\N	0	2019-06-15	00:03:21	https://coverartarchive.org/release/2fa17006-1e3b-4cc7-bf9e-adca94e1db35/39244186248-250.jpg
28	Yah Mean	Імпортовано з MusicBrainz (ID: d6ce9eea-e234-4166-b931-d4610b1fde45)	2025-10-31 14:44:35.929054+00	6	\N	18	\N	0	2018-12-12	00:02:46	http://coverartarchive.org/release/eb08ad6b-c6d5-47be-81fc-959fb02f387c/37514136270-250.jpg
14	Burn Out	Імпортовано з MusicBrainz (ID: 9af29e71-e348-46ec-9390-a47f2fc5242b)	2025-10-31 14:42:26.064434+00	5	\N	6	\N	0	2017-07-20	00:04:34	https://coverartarchive.org/release/2fa17006-1e3b-4cc7-bf9e-adca94e1db35/39244186248-250.jpg
53	Love Machine	Zaimportowano z MusicBrainz (ID: eb55876d-d83a-491c-9707-591ee136223d)	2025-10-31 22:14:32.743132+00	10	3	29	\N	0	2025-01-30	00:03:37	\N
59	From the Ritz to the Rubble	Zaimportowano z MusicBrainz (ID: 6c38a025-0a0b-46e7-bd90-460a82feae70)	2025-10-31 22:14:35.190883+00	10	3	1	73.33333333333333	1	2006-11-29	00:03:13.426	\N
30	Keep My Coo	Zaimportowano z MusicBrainz (ID: 15656b8a-e2f0-479a-ba65-12a2caa763cd)	2025-10-31 21:03:40.707273+00	7	\N	28	93.33333333333333	1	2019-11-15	00:04:26.187	http://coverartarchive.org/release/693b65bf-dabe-4291-994f-08f9c745e3d3/28313784219-250.jpg
51	A Little Death	Zaimportowano z MusicBrainz (ID: d11d62e9-dcb5-4632-b34f-453439a56f49)	2025-10-31 22:13:43.314587+00	9	3	1	\N	0	2013-04-22	00:03:29	http://coverartarchive.org/release/b3345720-eb66-4f58-949b-71426b215c33/28311828711-250.jpg
56	Dancing Shoes	Zaimportowano z MusicBrainz (ID: cd4f354c-63a5-469b-932f-0c38aeaeeea3)	2025-10-31 22:14:34.000888+00	10	3	1	\N	0	2006-11-29	00:02:21.133	\N
57	7	Zaimportowano z MusicBrainz (ID: e9ad7478-2cdf-47d6-b7c0-bb23cdd66bb4)	2025-10-31 22:14:34.402822+00	10	3	1	\N	0	2007-01-01	00:02:10	\N
58	Still Take You Home	Zaimportowano z MusicBrainz (ID: bd51a089-193a-4d25-bc7f-81ac84924043)	2025-10-31 22:14:34.816132+00	10	3	1	\N	0	2006-11-29	00:02:53.666	\N
60	Fake Tales of San Francisco	Zaimportowano z MusicBrainz (ID: 251c24cc-eb0f-4a17-a5dd-88e0008536d6)	2025-10-31 22:14:35.587875+00	10	3	1	\N	0	2005-11-01	00:02:57.946	\N
63	Cyclopean Edifice	Zaimportowano z MusicBrainz (ID: 47885e62-0878-4f33-8f14-f3c242cc6d61)	2025-10-31 22:15:16.738039+00	11	3	15	\N	0	2013-01-31	00:05:23	\N
62	The View From the Afternoon	Zaimportowano z MusicBrainz (ID: 40585e68-e030-4bd9-9a97-d359ce3f5f98)	2025-10-31 22:14:36.460871+00	10	3	21	\N	0	2009-01-01	00:04:20	\N
61	Mardy Bum	Zaimportowano z MusicBrainz (ID: 739a8662-e2bc-4ae3-bf7f-01ed5c4d3ad3)	2025-10-31 22:14:36.048012+00	10	3	51	\N	0	2009-01-01	00:04:01	\N
55	Perhaps Vampires Is a Bit Strong But...	Zaimportowano z MusicBrainz (ID: 828d9ad9-b868-4c4d-8c8d-fb58340b6da1)	2025-10-31 22:14:33.584895+00	10	3	32	\N	0	2009-01-01	00:03:22	\N
54	Bigger Boys and Stolen Sweethearts	Zaimportowano z MusicBrainz (ID: 28bf5abb-7aa1-490d-a1e7-02a37f145f01)	2025-10-31 22:14:33.202899+00	10	3	47	\N	0	2009-01-01	00:03:12	\N
52	Sweater Weather	Zaimportowano z MusicBrainz (ID: cc43f048-1585-4d66-b5aa-9583082c9719)	2025-10-31 22:13:45.594749+00	9	3	35	\N	0	2012-07-05	\N	http://coverartarchive.org/release/9e741fa7-22af-4dd2-a0f9-29c9c7cc43c0/32131583360-250.jpg
50	Pretty Boy	Zaimportowano z MusicBrainz (ID: 18c2388f-1bc9-404a-bf2f-2c3c844c1d6e)	2025-10-31 22:13:40.745885+00	9	3	4	\N	0	2020-11-27	00:03:54.093	http://coverartarchive.org/release/6e4d115e-26dc-4c08-a631-9ff8c3827fdc/30531201226-250.jpg
49	Sweater Weather (radio edit)	Zaimportowano z MusicBrainz (ID: 01befc0b-9125-47c7-8567-921d4bfedc5f)	2025-10-31 22:13:38.514238+00	9	3	33	\N	0	2015-12-12	00:03:39	http://coverartarchive.org/release/ec38fa85-4914-4117-92a4-7bd699182701/29754616662-250.jpg
48	Let It Go	Zaimportowano z MusicBrainz (ID: 1837c1f3-7a9a-478a-87e1-a470db2bcf98)	2025-10-31 22:13:36.204236+00	9	3	49	\N	0	2012-12-18	00:03:17.267	http://coverartarchive.org/release/991a4566-784d-452a-8d12-d5226253ef07/6357329224-250.jpg
47	Big Long Line	Zaimportowano z MusicBrainz (ID: 83fa6da9-5eee-4c43-adb2-8f8abc5910e1)	2025-10-31 22:13:34.087239+00	9	3	22	\N	0	1988-01-01	00:03:07	\N
46	That Way (instrumental)	Zaimportowano z MusicBrainz (ID: 6a69e626-1bbd-4b9f-98e6-c9244011cbd9)	2025-10-31 22:13:33.68428+00	9	3	23	\N	0	1989-01-01	00:03:58	\N
45	Missing Out	Zaimportowano z MusicBrainz (ID: 62aaae57-464a-46a7-a52d-98b47d44612e)	2025-10-31 22:13:33.273285+00	9	3	34	\N	0	1989-01-01	00:06:10	\N
44	A The Time (B the Inclination)	Zaimportowano z MusicBrainz (ID: 505dd9c7-ecc3-4d43-aafa-da1a96975543)	2025-10-31 22:13:32.891935+00	9	3	50	\N	0	2001-01-01	00:03:33	\N
43	No!	Zaimportowano z MusicBrainz (ID: fb4b5d32-0a10-422d-9c2a-55c91c4ff09e)	2025-10-31 22:12:35.068639+00	8	3	40	\N	0	2025-08-29	00:01:51	https://coverartarchive.org/release/2619675f-21fc-490d-a3d4-1c4e0bdb3814/42908857157-250.jpg
42	Bad Dream	Zaimportowano z MusicBrainz (ID: 989d3ae5-5b0b-4ea9-8568-3f39169e53d5)	2025-10-31 22:12:31.975483+00	8	3	10	\N	0	2025-08-29	00:02:40	https://coverartarchive.org/release/2619675f-21fc-490d-a3d4-1c4e0bdb3814/42908857157-250.jpg
41	CAROLINE	Zaimportowano z MusicBrainz (ID: d11ef345-8e50-42e8-a5b7-cd32fe311eff)	2025-10-31 22:12:28.711672+00	8	3	3	\N	0	2023-09-15	00:03:12.951	http://coverartarchive.org/release/03c9f4b5-9111-4ab9-bdea-d7f944e55485/34608537156-250.jpg
40	Knocking At My Door	Zaimportowano z MusicBrainz (ID: 3d815be5-ba13-4f62-984f-8490180e4528)	2025-10-31 22:12:24.017198+00	8	3	2	\N	0	2023-08-23	00:03:29	https://coverartarchive.org/release/39a25b3d-1693-4ade-ad5c-d339409c9bf6/42506998067-250.jpg
39	Waste My Mind	Zaimportowano z MusicBrainz (ID: 6d10a0f7-818e-4b0a-bb3d-6255ff86c937)	2025-10-31 22:12:21.47679+00	8	3	11	\N	0	2023-06-15	00:02:42	https://coverartarchive.org/release/0bcdbfe4-b7fd-4fce-90be-074558d0ee2a/42506929023-250.jpg
38	Awfully Sad	Zaimportowano z MusicBrainz (ID: cae0d1cd-8ae5-4a28-8dc2-f805259a1b80)	2025-10-31 22:12:18.729866+00	8	3	36	\N	0	2025-08-29	00:02:23	https://coverartarchive.org/release/2619675f-21fc-490d-a3d4-1c4e0bdb3814/42908857157-250.jpg
37	I'll Love Who I'll Love	Zaimportowano z MusicBrainz (ID: 39eed367-a57e-4bd3-b925-afed1680547c)	2025-10-31 22:12:15.626641+00	8	3	18	\N	0	2025-08-29	00:02:45	https://coverartarchive.org/release/2619675f-21fc-490d-a3d4-1c4e0bdb3814/42908857157-250.jpg
36	Aim For The Bushes	Zaimportowano z MusicBrainz (ID: e589745c-97e5-41ee-8d0f-5af8976db395)	2025-10-31 22:12:12.482409+00	8	3	26	\N	0	2025-08-29	00:03:20	https://coverartarchive.org/release/2619675f-21fc-490d-a3d4-1c4e0bdb3814/42908857157-250.jpg
35	A Sharp Pain	Zaimportowano z MusicBrainz (ID: fda39b54-4801-4f5a-9686-82724cb33409)	2025-10-31 22:12:09.351761+00	8	3	21	\N	0	2025-08-29	00:03:38	https://coverartarchive.org/release/2619675f-21fc-490d-a3d4-1c4e0bdb3814/42908857157-250.jpg
34	Knocking at My Door	Zaimportowano z MusicBrainz (ID: 19e6d39e-280f-4d59-a36c-7676399acff0)	2025-10-31 22:12:05.558572+00	8	3	31	\N	0	2024-01-16	00:03:10.433	https://coverartarchive.org/release/7880302b-b320-430e-83ef-cc6be5a60f58/41525366254-250.jpg
66	Bikinis	Zaimportowano z MusicBrainz (ID: df81e060-c494-4db6-ace9-29e8afe07768)	2025-10-31 22:15:22.278601+00	12	3	20	\N	0	2024-06-18	00:03:15.767	https://coverartarchive.org/release/278c82eb-37e7-4692-8e1f-d21ee914235c/40633134857-250.jpg
64	Driving Me Wild	Zaimportowano z MusicBrainz (ID: f763173d-012a-4800-9889-f310c50ed9cf)	2025-10-31 22:15:18.927621+00	11	3	42	\N	0	1993-01-01	00:02:38.093	http://coverartarchive.org/release/74b45379-9099-4d6c-97b9-b5ed0ca9b544/7953300238-250.jpg
26	Long Time (intro)	Імпортовано з MusicBrainz (ID: e3514e21-5721-4947-8d48-c6feec2347b7)	2025-10-31 14:44:31.024975+00	6	\N	2	\N	0	2025-08-19	00:03:32	http://coverartarchive.org/release/8b72aa31-3033-4861-8f99-ed6debf30a1e/37514067918-250.jpg
85	Forever (Slowed Down)	Zaimportowano z MusicBrainz (ID: 18bb471c-1f0f-4be6-8314-5e20084e31ad)	2026-01-04 13:35:02.994028+00	14	3	17	45	1	2019-03-08	00:02:00.914	\N
77	EMPTY BOULEVARDS	Zaimportowano z MusicBrainz (ID: 6cc5c399-2f6d-416d-9e1a-6866878558ed)	2025-11-01 16:16:19.189889+00	2	3	11	26.666666666666668	1	2022-08-05	00:01:45	\N
69	1000 Lies	Zaimportowano z MusicBrainz (ID: 07f78cf9-b3cc-43a6-a7da-e61248cc5b58)	2025-10-31 22:15:29.339103+00	11	3	29	\N	0	2023-03-09	00:02:09	http://coverartarchive.org/release/e0924f4d-c2b4-4d32-8d5a-6d492e89867b/35959352488-250.jpg
73	stairway to our window	Zaimportowano z MusicBrainz (ID: 710bac26-b098-447a-afb7-0dab10cdb7fe)	2025-11-01 16:15:55.845182+00	2	3	7	8.333333333333332	1	2022-08-05	00:03:12	https://coverartarchive.org/release/a74ff139-ac50-42ec-aa2f-9103d207a229/38707193975-250.jpg
67	Us	Zaimportowano z MusicBrainz (ID: f81a6e4c-eb15-416f-b7ac-a2d56b6c6e47)	2025-10-31 22:15:24.670874+00	12	3	21	65	1	2024-09-13	00:03:41.538	https://coverartarchive.org/release/bb0ac386-d9b4-4b35-ba32-efa5c82e7e91/39923020823-250.jpg
70	Deserts of Eternity	Zaimportowano z MusicBrainz (ID: 3c86b080-df27-4602-92f0-29f5e847764e)	2025-10-31 22:15:31.567538+00	11	3	29	71.66666666666667	1	2020-06-28	00:07:01	http://coverartarchive.org/release/8b950166-0999-4616-877d-e9f3473fbcd5/33993143172-250.jpg
74	WASTED	Zaimportowano z MusicBrainz (ID: a053ea8a-c121-465d-9a80-a0fd922512c7)	2025-11-01 16:15:57.803151+00	2	3	18	38.333333333333336	1	2022-08-05	00:03:20	https://coverartarchive.org/release/a74ff139-ac50-42ec-aa2f-9103d207a229/38707193975-250.jpg
68	Untitled	Zaimportowano z MusicBrainz (ID: 1ac36a0f-9c71-4a5f-b067-5344c7966224)	2025-10-31 22:15:26.965552+00	11	3	50	47.5	2	2011-02-21	00:20:00	http://coverartarchive.org/release/7c34937e-7294-4513-9141-a93b852d0fd5/35783970587-250.jpg
72	Utterance Beyond Death	Zaimportowano z MusicBrainz (ID: 31c14040-9822-4a0b-9483-ef5f6224f4cb)	2025-10-31 22:15:36.473548+00	11	3	29	55.00000000000001	1	2022-06-20	00:04:41	http://coverartarchive.org/release/578fa511-1093-486b-af99-af93f8b481cd/33993139904-250.jpg
71	Execration Rites	Zaimportowano z MusicBrainz (ID: 7db413ee-5e35-49e2-89d9-7f970f722d09)	2025-10-31 22:15:34.305749+00	11	3	29	\N	0	2022-03-08	00:03:20	http://coverartarchive.org/release/8b950166-0999-4616-877d-e9f3473fbcd5/33993143172-250.jpg
2	Young KId		2025-10-29 23:06:04.872238+00	2	3	2	60.83333333333333	6	2025-05-13	00:03:21	\N
83	Love & Affection	Zaimportowano z MusicBrainz (ID: 0ffa81d3-fa36-40eb-930c-f8c9cc5a9ea0)	2026-01-04 13:35:02.289678+00	14	3	31	\N	0	2021-11-13	00:01:27.7	\N
87	Life Is Pointless	Zaimportowano z MusicBrainz (ID: a352e537-d301-47cf-8a03-b5aa83a248d7)	2026-01-04 13:35:03.656785+00	14	3	46	\N	0	2022-12-22	00:01:41.054	\N
86	Forever	Zaimportowano z MusicBrainz (ID: d6f9fa65-c3fb-47df-b877-ded15acd0fdc)	2026-01-04 13:35:03.36733+00	14	3	1	\N	0	2019-03-08	00:01:48.696	\N
84	Marceline	Zaimportowano z MusicBrainz (ID: 2420200b-5c84-4d72-8872-785b337aeee1)	2026-01-04 13:35:02.583205+00	14	3	10	43.333333333333336	1	2021-11-13	00:02:27.096	\N
75	Late Nights	Zaimportowano z MusicBrainz (ID: 17922c2e-7548-4a7b-9f35-fcfad17eb464)	2025-11-01 16:16:00.730418+00	2	3	16	76.66666666666667	1	2021-12-01	00:03:41	https://coverartarchive.org/release/48f94400-f2b0-41a2-ac27-3680b91de614/38707310072-250.jpg
\.


ALTER TABLE public.music_track ENABLE TRIGGER ALL;

--
-- Data for Name: music_favorite; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.music_favorite DISABLE TRIGGER ALL;

COPY public.music_favorite (id, created_at, track_id, user_id) FROM stdin;
64	2025-11-20 22:17:26.708697+00	68	16
65	2025-11-20 22:17:38.657808+00	72	16
66	2025-11-27 00:47:51.262315+00	74	3
81	2025-12-22 22:48:44.310151+00	2	3
83	2025-12-29 15:25:57.397167+00	72	3
88	2025-12-29 15:28:37.776446+00	77	3
91	2025-12-29 15:28:49.607004+00	64	3
101	2026-01-07 13:39:45.475061+00	51	3
47	2025-11-08 03:18:19.374303+00	70	3
49	2025-11-08 03:18:22.206546+00	69	3
50	2025-11-08 03:18:22.95209+00	67	3
55	2025-11-08 12:32:06.896944+00	73	3
57	2025-11-09 21:51:48.141937+00	68	3
\.


ALTER TABLE public.music_favorite ENABLE TRIGGER ALL;

--
-- Data for Name: music_playlisttrack; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.music_playlisttrack DISABLE TRIGGER ALL;

COPY public.music_playlisttrack (id, "position", added_at, playlist_id, track_id) FROM stdin;
2	0	2025-11-08 03:18:19.380309+00	2	70
4	2	2025-11-08 03:18:22.21255+00	2	69
5	3	2025-11-08 03:18:22.957094+00	2	67
78	6	2025-12-22 22:48:44.317153+00	2	2
15	0	2025-11-08 12:34:38.282766+00	1	2
62	1	2025-12-01 17:43:40.258796+00	1	75
13	4	2025-11-08 12:32:06.90395+00	2	73
80	7	2025-12-29 15:25:57.408374+00	2	72
18	6	2025-11-09 21:51:48.146942+00	2	68
85	8	2025-12-29 15:28:37.783735+00	2	77
88	9	2025-12-29 15:28:49.613004+00	2	64
96	2	2026-01-06 23:30:02.199404+00	1	83
97	3	2026-01-06 23:30:06.831626+00	1	74
33	0	2025-11-18 13:52:57.627928+00	9	74
98	4	2026-01-06 23:30:13.343091+00	1	70
99	5	2026-01-06 23:30:29.384641+00	1	68
100	6	2026-01-06 23:30:52.220621+00	1	66
37	1	2025-11-19 23:44:36.475537+00	13	71
101	7	2026-01-06 23:30:59.518397+00	1	69
40	0	2025-11-20 22:17:26.716843+00	17	68
41	1	2025-11-20 22:17:29.75903+00	16	68
42	2	2025-11-20 22:17:36.444567+00	16	72
43	1	2025-11-20 22:17:38.664814+00	17	72
44	1	2025-11-20 22:24:04.396213+00	18	77
45	2	2025-11-20 22:24:07.895848+00	18	67
46	3	2025-11-20 22:24:22.902952+00	18	31
103	8	2026-01-06 23:31:10.799088+00	1	50
104	9	2026-01-06 23:31:19.35555+00	1	49
105	1	2026-01-06 23:36:42.313933+00	26	73
50	6	2025-11-27 00:47:51.27332+00	2	74
106	2	2026-01-06 23:36:45.402657+00	26	71
52	0	2025-11-27 00:53:09.966808+00	5	2
108	10	2026-01-07 13:39:45.481062+00	2	51
109	1	2026-01-14 02:23:25.075103+00	27	87
38	0	2025-11-20 15:50:01.073985+00	14	77
54	1	2025-11-27 00:53:12.24791+00	14	2
49	0	2025-11-23 14:37:41.690687+00	12	68
51	1	2025-11-27 00:53:03.023946+00	12	2
55	0	2025-11-27 00:53:13.776889+00	19	2
68	1	2025-12-22 00:01:40.558774+00	19	75
69	2	2025-12-22 00:02:02.387663+00	14	75
71	0	2025-12-22 00:09:28.843554+00	6	75
\.


ALTER TABLE public.music_playlisttrack ENABLE TRIGGER ALL;

--
-- Data for Name: music_review; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.music_review DISABLE TRIGGER ALL;

COPY public.music_review (id, text, created_at, updated_at, track_id, user_id, atmosphere_vibe, individuality, rhyme_imagery, structure_rhythm, style_execution, trend_relevance, title) FROM stdin;
17	super	2025-11-02 16:15:02.868644+00	2025-11-02 16:15:47.305681+00	67	3	7	9	4	6	8	5	blade
19		2025-11-04 12:53:32.088208+00	2025-11-04 12:53:32.088208+00	68	3	0	0	0	9	9	0	
5		2025-10-29 21:19:12.188785+00	2025-10-30 10:33:51.616837+00	1	3	10	9	6	8	4	10	
21		2025-11-06 13:37:08.030693+00	2025-11-06 13:37:08.030693+00	73	3	0	0	5	0	0	0	
23	123	2025-11-09 21:40:34.161919+00	2025-11-09 21:40:44.875766+00	70	3	7	7	8	5	9	7	Cool
24		2025-11-17 16:59:21.112668+00	2025-11-17 16:59:21.112668+00	77	3	0	0	8	0	8	0	
28	Masterpiece	2025-11-20 22:16:08.982727+00	2025-11-20 22:16:08.982727+00	68	16	8	6	8	8	6	3	My opinion
29		2025-11-20 22:18:01.65396+00	2025-11-20 22:18:01.65396+00	72	16	3	7	8	4	7	4	
22	great	2025-11-06 14:10:03.596308+00	2025-11-28 14:46:36.442908+00	2	3	8	6	7	6	8	4	dsfsdfs
30		2025-11-28 14:54:12.534952+00	2025-11-28 14:56:02.661218+00	59	3	8	8	8	5	8	7	
9	qweqweqweqweqw	2025-10-30 22:00:39.544348+00	2025-10-30 22:00:39.544348+00	2	4	3	3	3	3	3	3	
10	ghdfhjfgjfgjfgj	2025-10-30 22:00:52.474466+00	2025-10-30 22:00:52.474466+00	2	7	5	5	5	5	5	5	
11	wfsdhdfhdfhdfh	2025-10-30 22:01:06.910633+00	2025-10-30 22:01:06.910633+00	2	8	7	7	7	7	7	7	
12	agdfjhnfgkjmghjfghfg	2025-10-30 22:01:21.203163+00	2025-10-30 22:01:21.203163+00	2	2	9	9	9	9	9	9	
15	jhgjkghkghkgh	2025-10-30 22:02:13.031598+00	2025-10-30 22:02:13.031598+00	2	1	6	6	6	6	6	6	
8		2025-10-30 21:49:46.645819+00	2026-01-06 21:25:30.134751+00	3	3	1	0	0	0	1	5	
16	dsgsdgsg	2025-10-31 21:06:06.957741+00	2026-01-06 21:25:58.470481+00	30	3	10	10	10	9	10	7	dsfsdfsdf
32		2026-01-07 13:39:38.125478+00	2026-01-07 13:39:38.125478+00	74	3	9	0	0	0	8	6	
33		2026-01-09 11:39:18.291883+00	2026-01-09 11:39:18.291883+00	84	3	8	0	7	0	7	4	
25		2025-11-17 16:59:31.289868+00	2026-01-19 13:25:13.277288+00	75	3	7	6	10	6	10	7	
34	sad	2026-01-19 13:25:37.84561+00	2026-01-19 13:25:37.84561+00	85	3	0	5	8	0	7	7	asd
\.


ALTER TABLE public.music_review ENABLE TRIGGER ALL;

--
-- Data for Name: music_reviewlike; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.music_reviewlike DISABLE TRIGGER ALL;

COPY public.music_reviewlike (id, created_at, review_id, user_id) FROM stdin;
65	2025-11-08 10:38:51.156594+00	17	3
66	2025-11-08 11:15:19.438652+00	15	3
68	2025-11-08 16:27:57.065825+00	9	3
70	2025-11-09 21:40:56.344716+00	23	3
14	2025-10-31 01:37:08.345962+00	11	3
76	2025-11-20 22:16:20.171079+00	19	16
77	2025-11-20 22:16:21.69136+00	28	16
78	2025-11-20 22:16:49.887859+00	22	16
21	2025-10-31 21:06:08.541528+00	16	3
83	2025-11-28 12:17:34.498231+00	12	3
27	2025-11-01 15:48:48.348484+00	8	2
28	2025-11-01 16:21:22.996782+00	5	3
90	2025-11-28 14:45:10.666046+00	10	3
91	2025-11-28 14:54:14.71032+00	30	3
92	2025-11-28 15:19:01.611851+00	24	3
95	2025-12-22 22:44:49.851699+00	22	3
96	2025-12-22 22:49:25.725517+00	22	2
48	2025-11-04 13:50:00.979213+00	19	3
61	2025-11-06 14:15:23.330377+00	8	3
\.


ALTER TABLE public.music_reviewlike ENABLE TRIGGER ALL;

--
-- Data for Name: users_errorreport; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.users_errorreport DISABLE TRIGGER ALL;

COPY public.users_errorreport (id, title, description, page_url, status, admin_notes, created_at, updated_at, resolved_at, resolved_by_id, user_id, content_id, content_type, report_reason) FROM stdin;
1	profile picture	123	http://127.0.0.1:8000/users/profile/	resolved	123123123	2025-11-10 19:53:38.96751+00	2025-11-10 19:54:26.315641+00	2025-11-10 19:54:26.315641+00	3	3	\N	general	
2	Zgłoszenie: Profil użytkownika: test2	jkljk	http://127.0.0.1:8000/users/report/profile/5/	resolved		2025-11-11 00:03:15.720896+00	2025-11-11 00:04:04.638076+00	2025-11-11 00:04:04.638076+00	3	3	5	profile	spam
3	Nieodpowiednia recenzja: Execration Rites	Zgłoszenie treści jako: Mowa nienawiści	http://127.0.0.1:8000/71/	pending		2025-11-11 00:56:51.40815+00	2025-11-11 00:56:51.40815+00	\N	\N	3	18	review	hate_speech
4	Nieodpowiednia recenzja: stairway to our window	Zgłoszenie treści jako: Molestowanie/Nękanie	http://127.0.0.1:8000/73/	in_progress		2025-11-11 01:01:50.647653+00	2025-11-12 15:03:49.171028+00	\N	\N	3	21	review	harassment
8	Zgłoszenie: Recenzja utworu: Untitled	Look	http://127.0.0.1:8000/users/report/review/19/	in_progress	We will fix it asd	2025-11-20 22:16:36.347494+00	2025-11-28 22:34:18.268492+00	\N	\N	16	19	review	spam
9	Zgłoszenie: Profil użytkownika: Oleksandr1	Zgłoszenie treści jako: Mowa nienawiści	http://127.0.0.1:8000/users/report/profile/16/	pending		2026-01-06 01:36:35.790083+00	2026-01-06 01:36:35.790083+00	\N	\N	3	16	profile	hate_speech
10	Nieodpowiednia recenzja: EMPTY BOULEVARDS	Zgłoszenie treści jako: Mowa nienawiści	http://127.0.0.1:8000/77/	pending		2026-01-06 01:37:45.612715+00	2026-01-06 01:37:45.612715+00	\N	\N	3	24	review	hate_speech
\.


ALTER TABLE public.users_errorreport ENABLE TRIGGER ALL;

--
-- Data for Name: users_user_groups; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.users_user_groups DISABLE TRIGGER ALL;

COPY public.users_user_groups (id, user_id, group_id) FROM stdin;
\.


ALTER TABLE public.users_user_groups ENABLE TRIGGER ALL;

--
-- Data for Name: users_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.users_user_user_permissions DISABLE TRIGGER ALL;

COPY public.users_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


ALTER TABLE public.users_user_user_permissions ENABLE TRIGGER ALL;

--
-- Data for Name: users_userblock; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.users_userblock DISABLE TRIGGER ALL;

COPY public.users_userblock (id, created_at, blocked_id, blocker_id) FROM stdin;
\.


ALTER TABLE public.users_userblock ENABLE TRIGGER ALL;

--
-- Data for Name: users_userfollow; Type: TABLE DATA; Schema: public; Owner: musicuser
--

ALTER TABLE public.users_userfollow DISABLE TRIGGER ALL;

COPY public.users_userfollow (id, created_at, follower_id, following_id) FROM stdin;
16	2025-11-20 22:18:34.521626+00	16	2
17	2025-11-20 22:18:55.34169+00	16	3
22	2025-12-23 01:42:01.664418+00	3	2
24	2026-01-07 13:54:30.164765+00	3	5
\.


ALTER TABLE public.users_userfollow ENABLE TRIGGER ALL;

--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 132, true);


--
-- Name: chat_chatparticipant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.chat_chatparticipant_id_seq', 14, true);


--
-- Name: chat_conversation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.chat_conversation_id_seq', 7, true);


--
-- Name: chat_groupchatmessage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.chat_groupchatmessage_id_seq', 23, true);


--
-- Name: chat_groupchatread_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.chat_groupchatread_id_seq', 14, true);


--
-- Name: chat_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.chat_message_id_seq', 64, true);


--
-- Name: chat_messageread_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.chat_messageread_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 154, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 33, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 54, true);


--
-- Name: events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.events_event_id_seq', 22, true);


--
-- Name: events_eventattendee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.events_eventattendee_id_seq', 51, true);


--
-- Name: events_eventpoll_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.events_eventpoll_id_seq', 14, true);


--
-- Name: events_eventrating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.events_eventrating_id_seq', 11, true);


--
-- Name: events_pollvote_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.events_pollvote_id_seq', 16, true);


--
-- Name: groups_group_genres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.groups_group_genres_id_seq', 34, true);


--
-- Name: groups_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.groups_group_id_seq', 13, true);


--
-- Name: groups_groupinvitation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.groups_groupinvitation_id_seq', 6, true);


--
-- Name: groups_groupmembership_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.groups_groupmembership_id_seq', 38, true);


--
-- Name: music_artist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.music_artist_id_seq', 14, true);


--
-- Name: music_favorite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.music_favorite_id_seq', 101, true);


--
-- Name: music_genre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.music_genre_id_seq', 55, true);


--
-- Name: music_playlist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.music_playlist_id_seq', 27, true);


--
-- Name: music_playlisttrack_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.music_playlisttrack_id_seq', 109, true);


--
-- Name: music_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.music_review_id_seq', 34, true);


--
-- Name: music_reviewlike_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.music_reviewlike_id_seq', 96, true);


--
-- Name: music_track_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.music_track_id_seq', 87, true);


--
-- Name: users_errorreport_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.users_errorreport_id_seq', 10, true);


--
-- Name: users_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.users_user_groups_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.users_user_id_seq', 16, true);


--
-- Name: users_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.users_user_user_permissions_id_seq', 1, false);


--
-- Name: users_userblock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.users_userblock_id_seq', 12, true);


--
-- Name: users_userfollow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: musicuser
--

SELECT pg_catalog.setval('public.users_userfollow_id_seq', 24, true);


--
-- PostgreSQL database dump complete
--

\unrestrict Mqlrf3jD8gDCchmbq1zrJcL4Dni6OXeoWllbSid0L180CzsMaXwSvsAQUW0BmEE

