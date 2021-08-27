-- FROM ds DATABASE EXECUTE

-- Admin
insert into users (name, surname, email, password, role) values ('Gino', 'Buonvino', 'gino@buonvino.com', '123', 'admin');

-- Roles
drop user if exists admin;
create user admin with password 'password';

drop user if exists panelist;
create user panelist with password 'password';

-- Users
grant SELECT ON users TO admin, panelist;
grant INSERT ON users TO admin, panelist;
grant UPDATE ON users TO admin, panelist;
grant DELETE ON users TO admin;

-- Surveys
grant SELECT ON surveys TO admin, panelist;
grant INSERT ON surveys TO admin;
grant UPDATE ON surveys TO admin;
grant DELETE ON surveys TO admin;

-- Questions
grant SELECT ON questions TO admin, panelist;
grant INSERT ON questions TO admin;
grant UPDATE ON questions TO admin;
grant DELETE ON questions TO admin;


-- Answers
grant SELECT ON answers TO admin, panelist;
grant INSERT ON answers TO admin;
grant UPDATE ON answers TO admin;
grant DELETE ON answers TO admin;

-- Fillings
grant SELECT ON fillings TO admin, panelist;
grant INSERT ON fillings TO panelist;
grant UPDATE ON fillings TO panelist;
grant DELETE ON fillings TO admin;

-- Responses
grant SELECT ON responses TO admin, panelist;
grant INSERT ON responses TO panelist;
grant UPDATE ON responses TO panelist;
grant DELETE ON responses TO admin;

-- Referencing permissions
GRANT TRUNCATE, REFERENCES, TRIGGER ON surveys TO admin, panelist;
GRANT TRUNCATE, REFERENCES, TRIGGER ON users TO admin, panelist;
GRANT TRUNCATE, REFERENCES, TRIGGER ON answers TO admin, panelist;
GRANT TRUNCATE, REFERENCES, TRIGGER ON questions TO admin, panelist;
GRANT TRUNCATE, REFERENCES, TRIGGER ON fillings TO admin, panelist;
GRANT TRUNCATE, REFERENCES, TRIGGER ON responses TO admin, panelist;

-- GRANT USAGE - For sequences, this privilege allows the use of the currval and nextval functions.
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ds;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO admin;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO panelist;
