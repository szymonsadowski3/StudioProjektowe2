create table section
(
  section_id   serial not null
    constraint section_pkey
    primary key,
  section_name varchar(255),
  section_logo text
);

create table thread
(
  thread_id          serial not null
    constraint thread_pkey
    primary key,
  thread_name        text,
  created_by_user_id integer,
  created_on         timestamp
);

create table thread_followers
(
  thread_id   integer,
  follower_id integer
);

create table "user"
(
  user_id    serial not null
    constraint user_pkey
    primary key,
  username   varchar(255),
  created_on timestamp,
  avatar     text,
  about_me   text,
  signature  text
);

create table user_group
(
  user_group_id   serial not null
    constraint user_group_pkey
    primary key,
  user_group_name varchar(255),
  about_group     text
);

create table user_group_belonging
(
  user_id       integer,
  user_group_id integer
);

create table post
(
  post_id          serial not null
    constraint post_pkey
    primary key,
  post_name        text,
  post_content     text,
  created_on       timestamp,
  parent_thread_id integer
);

