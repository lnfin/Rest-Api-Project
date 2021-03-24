create database yandex_db;
create user yandex_app with encrypted password 'sup3r_s3cr3t_p4ss';
grant all privileges on database yandex_db to yandex_app;

psql -U yandex_app -W -d yandex_db

CREATE TABLE couriers (
    id serial PRIMARY KEY, 
    courier_type varchar (10) NOT NULL,
    regions integer ARRAY,
    working_hours text ARRAY
);

CREATE TABLE orders(
    id serial PRIMARY KEY,
    weight  float NOT NULL,
    region integer NOT NULL,
    delivery_hours text ARRAY
);