\c sandrina
SET ROLE TO sandrina;
CREATE TABLE lavoro (
    id bigserial PRIMARY KEY, 
    comune_id bigint REFERENCES comuni (id),
    mese integer,
    anno integer,
    entry jsonb
);
