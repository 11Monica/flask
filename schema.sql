drop table if exists persons;
create table persons (
  id integer primary key autoincrement,
  name text not null,
  studentid  integer not null,
  sex  text not null,
  tel text not null,
  emile  text not null,
  class text not null,
  department  text not null,
  self_introduction  text not null

  
);
