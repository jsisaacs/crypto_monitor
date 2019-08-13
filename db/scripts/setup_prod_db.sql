drop database if exists crypto_prod_db;
drop table if exists crypto_prod_data;

create database crypto_prod_db;

create table crypto_prod_data (
  id serial primary key,
  subreddit varchar(20) not null,
  active_users integer not null,
  subreddit_sentiment numeric not null,
  currency_sentiment numeric not null,
  timestamp numeric not null
);

select *
from crypto_prod_data;