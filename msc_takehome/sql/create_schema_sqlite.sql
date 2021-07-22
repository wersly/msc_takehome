create table names (
  id integer primary key autoincrement,
  first_name varchar(255) not null,
  middle_name varchar(255),
  last_name varchar(255)
);

-- Q: should there be a unique index on instrument?
-- A: probably not, but it would make sense to have a unique constraint on the combination of instrument/section
-- ie, one instrument can exist in multiple different section designations, but that instrument should not be duplicated within its section
create table instruments (
  id integer primary key autoincrement,
  instrument varchar(255) not null,
  section varchar(255) not null,
  unique(instrument, section)
);

create table assignments_by_name(
  id integer primary key autoincrement,
  instrument varchar(255) not null,
  first_name varchar(255) not null,
  middle_name varchar(255),
  last_name varchar(255)
);

create table assignments (
  id integer primary key autoincrement,
  player_id integer not null,
  instrument_id integer not null,
  foreign key (player_id) references names(id),
  foreign key (instrument_id) references instruments(id)
);

-- REPORTS
-- 1. A report showing the name, instrument, and section for all musicians.
create view all_musicians as
  select
    n.first_name, n.middle_name , n.last_name , i.instrument , i.section
    from
      names n
      left join assignments a
          on n.id = a.player_id
      left join instruments i
          on i.id = a.instrument_id
   order by n.id, i.id asc;

-- 2. A report showing the instruments that don't yet have musicians (i.e. no one plays the trumpet), and their sections, sorted by section, alphabetically in ascending order.
create view instruments_without_musicians as
  select instrument , section
    from instruments i
   where id not in (select instrument_id from assignments)
   order by section asc;

-- 3. A report showing any musicians that play two or more instruments, their instrument, and section.
create view multi_instrumentalists as
  with instrument_count as (
    select player_id, instrument_id,
           count(instrument_id) over (partition by player_id) as num_instruments
      from assignments a
  ),
  multi_instrumentalists as (
    select *
      from instrument_count
     where num_instruments > 1
  )
  select n.first_name, n.middle_name , n.last_name , i.instrument , i.section
    from names n
         inner join multi_instrumentalists m
             on n.id = m.player_id
         inner join instruments i
             on i.id = m.instrument_id
   order by n.id, i.id asc;

-- 4. A report showing any instruments that are played by multiple musicians, as well as the musician names and sections.
create view multiple_players as
  with player_count as (
	  select player_id, instrument_id,
	         count(player_id) over (partition by instrument_id) as num_players
	    from assignments a
	),
	multiple_players as (
	  select *
	    from player_count
	   where num_players > 1
	)
	select i.instrument , i.section, n.first_name, n.middle_name , n.last_name
	  from names n
	       inner join multiple_players m
	           on n.id = m.player_id
	       inner join instruments i
	           on i.id = m.instrument_id
   order by i.id, n.id asc;
