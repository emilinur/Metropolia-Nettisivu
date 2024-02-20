create database users;

create table users (
    id int primary key,
    name varchar(255) not null,
    email varchar(255) not null,
    password varchar(255) not null,
    type ENUM('teacher','student') not null
);

create table courses (
    id int auto_increment primary key,
    name varchar(255) not null,
    credits int not null,
    teacherId int,
    foreign key (teacherId) references users(id)
);