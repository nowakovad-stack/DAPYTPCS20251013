-- create new users
create role student with login password 'Kurz-DAPYT_ST45';
create role robot with login password 'Kurz-DAPYT_ST45';

-- update default privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO student;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT,INSERT,DELETE ON TABLES TO robot;

-- grant RO for `ALL TABLES` (existing)
GRANT SELECT ON ALL TABLES IN SCHEMA public TO student;
-- grant RW for `ALL TABLES` (existing)
GRANT SELECT,INSERT,DELETE ON ALL TABLES IN SCHEMA public TO robot;
