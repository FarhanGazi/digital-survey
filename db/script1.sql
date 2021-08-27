-- Remove old database
drop database if exists ds;

-- Remove old ds app user
drop user if exists ds;

-- Create new ds app user
create user ds with password 'password';

-- Create new database
create database ds owner ds;
