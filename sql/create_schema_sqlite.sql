CREATE TABLE names (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name VARCHAR(255) NOT NULL,
  middle_name VARCHAR(255),
  last_name VARCHAR(255)
);

-- Q: should there be a unique index on instrument?
-- A: probably not, but it would make sense to have a unique constraint on the combination of instrument/section
-- ie, one instrument can exist in multiple different section designations, but that instrument should not be duplicated within its section
CREATE TABLE instruments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  instrument VARCHAR(255),
  section VARCHAR(255),
  UNIQUE(instrument, section)
);

CREATE TABLE assignments_by_name(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  instrument VARCHAR(255) NOT NULL,
  first_name VARCHAR(255) NOT NULL,
  middle_name VARCHAR(255),
  last_name VARCHAR(255)
);

CREATE TABLE assignments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  player_id INTEGER,
  instrument_id INTEGER,
  FOREIGN KEY (player_id) REFERENCES names(id),
  FOREIGN KEY (instrument_id) REFERENCES instruments(id)
);

-- REPORTS
-- 1. A report showing the name, instrument, and section for all musicians.
/*
  TODO: does this include people who are currently not assigned an instrument?
  TODO: how should we render people who play multiple instruments - as multiple rows, or as a single, compressed row?
*/
CREATE VIEW all_musicians AS
  SELECT
    n.first_name, n.middle_name , n.last_name , i.instrument , i.section
    FROM
      names n
      LEFT JOIN assignments a
          ON n.id = a.player_id
      LEFT JOIN instruments i
          ON i.id = a.instrument_id
   ORDER BY n.id, i.id ASC;

-- 2. A report showing the instruments that don't yet have musicians (i.e. no one plays the trumpet), and their sections, sorted by section, alphabetically in ascending order.
CREATE VIEW instruments_without_musicians AS
  SELECT instrument , section
    FROM instruments i
   WHERE id NOT IN (SELECT instrument_id FROM assignments)
   ORDER BY section ASC;

-- 3. A report showing any musicians that play two or more instruments, their instrument, and section.
CREATE VIEW multi_instrumentalists AS
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
CREATE VIEW multiple_players AS
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
