\c sandrina 
CREATE INDEX salute_fkey_idx ON salute USING btree(anno, mese);
CREATE INDEX on salute USING gin(entry jsonb_path_ops);
VACUUM ANALYZE salute;
