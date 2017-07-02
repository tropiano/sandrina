\c sandrina
SET ROLE TO sandrina;
CREATE TABLE startup (
    id bigserial PRIMARY KEY, 
    comune_id bigint REFERENCES comuni (id),
    mese integer,
    anno integer,
    entry jsonb
);
