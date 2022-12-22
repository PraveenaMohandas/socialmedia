# -- SIGNUP TABLE CREATION QUERY --

# CREATE TABLE IF NOT EXISTS public.signup
# (
#     userid integer NOT NULL,
#     first_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     last_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     email character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     password character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     gender character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     dob character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     CONSTRAINT signup_pkey PRIMARY KEY (userid)
# )
# WITH (
#     OIDS = FALSE
# )
# TABLESPACE pg_default;

# ALTER TABLE IF EXISTS public.signup
#     OWNER to postgres;


# -- FRIENDS TABLE CREATION QUERY --

# CREATE TABLE IF NOT EXISTS public.friends
# (
#     userid integer NOT NULL,
#     receiverid character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     status character varying(50) COLLATE pg_catalog."default" NOT NULL,
#     CONSTRAINT fk_signup FOREIGN KEY (userid)
#         REFERENCES public.signup (userid) MATCH SIMPLE
#         ON UPDATE NO ACTION
#         ON DELETE NO ACTION
# )
# WITH (
#     OIDS = FALSE
# )
# TABLESPACE pg_default;

# ALTER TABLE IF EXISTS public.friends
#     OWNER to postgres;