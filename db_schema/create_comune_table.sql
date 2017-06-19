\c sandrina
SET ROLE TO sandrina;
CREATE TABLE comuni (
    id bigserial PRIMARY KEY,
    codice_catastale text,
    codice_comune_103 text,
    codice_comune_107 text,
    nome text,
    regione text,
    provincia char(2)
);
