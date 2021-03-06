-- Roles
CREATE ROLE sandrina LOGIN PASSWORD 'v5sYvBKw';
CREATE ROLE sandrina_ro LOGIN PASSWORD 'v5sYvBKw';
CREATE ROLE sandrina_rw LOGIN PASSWORD 'v5sYvBKw' IN ROLE sandrina_ro; 

-- Database creation
CREATE DATABASE sandrina WITH OWNER sandrina ENCODING 'UTF8';

-- Database access privileges
REVOKE CONNECT ON DATABASE sandrina FROM PUBLIC;
GRANT CONNECT ON DATABASE sandrina TO sandrina;
GRANT CONNECT ON DATABASE sandrina TO sandrina_rw;
GRANT CONNECT ON DATABASE sandrina TO sandrina_ro;

-- Table access privileges
\c sandrina
SET ROLE TO sandrina;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON tables TO sandrina_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON sequences TO sandrina_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT UPDATE, INSERT, DELETE ON tables TO sandrina_rw;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT UPDATE ON sequences TO sandrina_rw;
