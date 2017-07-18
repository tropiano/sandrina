\c sandrina 
CREATE INDEX comuni_idx ON comuni USING btree (codice_catastale, codice_comune_103, codice_comune_107, nome);
VACUUM ANALYZE comuni;
