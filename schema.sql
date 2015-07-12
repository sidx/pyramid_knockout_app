create table if not exists details (
	id integer primary key autoincrement,
    mailid char(100) not null,
    name char(100) not null,
    phone integer(10) not null
);
