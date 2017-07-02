CREATE INDEX startup_fkey_idx ON startup(anno, mese) USING btree;
CREATE INDEX on startup(entry jsonb_path_ops) USING gin;
VACUUM ANALYZE startup;
