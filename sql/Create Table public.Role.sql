-- DDL generated by Postico 2.0.5
-- Not all database features are supported. Do not use for backup.

-- Table Definition ----------------------------------------------

CREATE TABLE "Role" (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name character varying(40) NOT NULL DEFAULT 'default name'::character varying
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX "Role_pkey" ON "Role"(id int4_ops);
