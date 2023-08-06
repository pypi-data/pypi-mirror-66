SELECT r.rolname AS user,
       t.relnamespace::regnamespace::name AS schema,
       t.relname::text AS name,
       p.perm AS permission
FROM pg_catalog.pg_class AS t
   CROSS JOIN pg_catalog.pg_roles AS r
   CROSS JOIN (VALUES ('SELECT'), ('USAGE'), ('UPDATE')) AS p(perm)
WHERE t.relnamespace::regnamespace::name <> 'information_schema'
  AND t.relnamespace::regnamespace::name NOT LIKE 'pg_%'
  AND r.rolname NOT LIKE 'pg_%'
  AND t.relkind = 'S'
  AND has_sequence_privilege(r.oid, t.oid, p.perm) = true
  AND NOT r.rolsuper;
