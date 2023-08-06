select * from (
    select
      table_schema as schema,
      table_name,
      column_name,
      grantee as user,
      privilege_type as privilege
    from information_schema.role_column_grants
    where grantee != (
        select tableowner
        from pg_tables
        where schemaname = table_schema
        and tablename = table_name
    )
-- SKIP_INTERNAL     and table_schema not in ('pg_internal', 'pg_catalog', 'information_schema', 'pg_toast')
-- SKIP_INTERNAL     and table_schema not like 'pg_temp_%' and table_schema not like 'pg_toast_temp_%'
    order by schema, table_name, column_name, user
) as column_privs
EXCEPT
select * from (
    select
      role_table_grants.table_schema as schema,
      role_table_grants.table_name as name,
      columns.column_name,
      role_table_grants.grantee as user,
      role_table_grants.privilege_type as privilege
    from information_schema.role_table_grants
    join information_schema.columns on columns.table_name = role_table_grants.table_name
    where grantee != (
        select tableowner
        from pg_tables
        where schemaname = role_table_grants.table_schema
        and tablename = role_table_grants.table_name
    )
    and role_table_grants.privilege_type != 'DELETE'
-- SKIP_INTERNAL    and role_table_grants.table_schema not in ('pg_internal', 'pg_catalog', 'information_schema', 'pg_toast')
-- SKIP_INTERNAL    and role_table_grants.table_schema not like 'pg_temp_%' and role_table_grants.table_schema not like 'pg_toast_temp_%'
    order by schema, name, column_name, user
) as table_privs;
