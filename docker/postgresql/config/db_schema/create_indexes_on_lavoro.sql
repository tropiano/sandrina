\c sandrina 
CREATE INDEX lavoro_fkey_idx ON lavoro USING btree(anno, mese);
CREATE INDEX on lavoro USING gin(entry jsonb_path_ops);
VACUUM ANALYZE lavoro;
