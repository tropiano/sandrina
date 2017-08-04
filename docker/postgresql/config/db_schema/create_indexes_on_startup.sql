\c sandrina 
CREATE INDEX startup_fkey_idx ON startup USING btree(anno, mese);
CREATE INDEX on startup USING gin(entry jsonb_path_ops);
VACUUM ANALYZE startup;
