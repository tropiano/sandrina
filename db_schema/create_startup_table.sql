\c sandrina
SET ROLE TO sandrina;
CREATE TABLE startup (
    id bigserial PRIMARY KEY, 
    comune_id bigint REFERENCES comune (id)
    mese integer,
    anno integer,
    entry jsonb
);
