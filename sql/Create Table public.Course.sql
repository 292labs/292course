-- DDL generated by Postico 2.0.5
-- Not all database features are supported. Do not use for backup.

-- Table Definition ----------------------------------------------

CREATE TABLE "Course" (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text,
    description text,
    column4 text
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX "Course_pkey" ON "Course"(id int4_ops);
