CREATE INDEX comuni_idx ON comuni(codice_catastale, codice_comune_103, codice_comune_107, nome) USING btree;
VACUUM ANALYZE comuni;
