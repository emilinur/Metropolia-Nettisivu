create database metropolia_nettisivu;

use metropolia_nettisivu;

create table users (
    id int auto_increment primary key,
    name varchar(255) not null,
    email varchar(255) not null,
    password varchar(255) not null,
    courses varchar(255),
    type ENUM('teacher','student') not null
);

create table courses (
    id int auto_increment primary key,
    name varchar(255) not null,
    credits int not null,
    teacherEmail int,
    foreign key (teacherId) references users(id)
);