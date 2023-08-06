select
    nspname as schema,
    r.rolname as user,
    pg_catalog.has_schema_privilege(r.rolname, nspname, 'CREATE') as create,
    pg_catalog.has_schema_privilege(r.rolname, nspname, 'USAGE') as usage
from pg_namespace pn, pg_catalog.pg_roles r
where array_to_string(nspacl,',') like '%'||r.rolname||'%' 
    and nspowner > 1
-- SKIP_INTERNAL and nspname <> 'information_schema'
-- SKIP_INTERNAL and nspname !~~ 'pg\_%'
order by schema, user;
