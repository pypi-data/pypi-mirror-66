select
  ur.rolname as roleid,
  um.rolname as member,
  a.admin_option,
  ug.rolname as grantor
from pg_auth_members a
left join pg_roles ur on ur.oid = a.roleid
left join pg_roles ug on ug.oid = a.grantor
left join pg_roles um on um.oid = a.member
where
    ur.rolname not like 'pg_%'
    and um.rolname not like 'pg_%'
    and ur.rolname not like 'rds%'
    and um.rolname not like 'rds%';
