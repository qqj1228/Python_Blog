-- init.sql

drop database if exists blogwebapp;

create database blogwebapp character set utf8;

use blogwebapp;

grant select, insert, update, delete on blogwebapp.* to 'qqj1228'@'localhost' identified by 'crkqj128';

create table user (
    `id` varchar(50) not null primary key,
    `email` varchar(50) not null,
    `password` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_at` real not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`)
) engine=innodb default charset=utf8;

create table blog (
    `id` varchar(50) not null primary key,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `cat_id` varchar(50),
    `cat_name` varchar(50),
    `title` varchar(50) not null,
    `summary` varchar(200) not null,
    `content` text not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`)
) engine=innodb default charset=utf8;

create table comment (
    `id` varchar(50) not null primary key,
    `blog_id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `content` text not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`)
) engine=innodb default charset=utf8;

create table category (
    `id` varchar(50) not null primary key,
    `name` varchar(50) not null,
    `created_at` real not null,
    unique key `idx_name` (`name`),
    key `idx_created_at` (`created_at`)
) engine=innodb default charset=utf8;
