# -- SIGNUP TABLE CREATION QUERY --

# CREATE TABLE IF NOT EXISTS public.users
# (
#     userid integer NOT NULL,
#     first_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     last_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     email character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     password character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     gender character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     dob character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     subscribed BOOLEAN NOT NULL,
#     CONSTRAINT users_pkey PRIMARY KEY (userid)
# )
# WITH (
#     OIDS = FALSE
# )
# TABLESPACE pg_default;

# ALTER TABLE IF EXISTS public.users
#     OWNER to postgres;


# -- FRIENDS TABLE CREATION QUERY --

# CREATE TABLE IF NOT EXISTS public.friends
# (
#     userid integer NOT NULL,
#     receiverid character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     status character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     CONSTRAINT fk_users FOREIGN KEY (userid)
#         REFERENCES public.users (userid) MATCH SIMPLE
#         ON UPDATE NO ACTION
#         ON DELETE NO ACTION
# )
# WITH (
#     OIDS = FALSE
# )
# TABLESPACE pg_default;

# ALTER TABLE IF EXISTS public.friends
#     OWNER to postgres;

# -- SAVE USER FEED TABLE

# CREATE TABLE IF NOT EXISTS public.userfeed
# (
#     id integer PRIMARY KEY NOT NULL,
#     userid integer NOT NULL,
#     title character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     description character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     image character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     tags character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     category character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     visibility character varying(20) COLLATE pg_catalog."default" NOT NULL,
#     deleted_at timestamp default null,
#     CONSTRAINT fk_users FOREIGN KEY (userid)
#         REFERENCES public.users (userid) MATCH SIMPLE
#         ON UPDATE NO ACTION
#         ON DELETE NO ACTION
# )
# WITH (
#     OIDS = FALSE
# )
# TABLESPACE pg_default;

# ALTER TABLE IF EXISTS public.userfeed
#     OWNER to postgres;


# -- RESET PASSWORD TABLE

# CREATE TABLE IF NOT EXISTS public.resetpassword
# (
#     id SERIAL primary key,
#     email character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     reset_token character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     requested_on timestamp default null
   
# )
# WITH (
#     OIDS = FALSE
# )
# TABLESPACE pg_default;

# ALTER TABLE IF EXISTS public.resetpassword
#     OWNER to postgres;