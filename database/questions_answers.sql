create table users
( id integer primary key autoincrement
, name text not null
, password text not null
, expert boolean not null
, admin boolean not null
) ;

create table questions 
( id integer primary key autoincrement
, question_text text not null
, questioned_by_id integer not null
, answer_text text not null
, answered_by_id integer not null
) ;
