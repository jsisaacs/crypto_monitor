drop database if exists crypto_dev_db;
drop table if exists crypto_data;

create database crypto_dev_db;

create table crypto_data (
  id serial primary key,
  subreddit varchar(20) not null,
  active_users integer not null,
  subreddit_sentiment numeric not null,
  currency_sentiment numeric not null,
  timestamp numeric not null
);

copy crypto_data (
  active_users,
  currency_sentiment, 
  subreddit, 
  subreddit_sentiment, 
  timestamp,
  id
)
from '/Users/joshisaacson/Desktop/crypo-monitor/db/test_data/crypto_data_dev.csv'
delimiter ',' csv header;

select *
from crypto_data;