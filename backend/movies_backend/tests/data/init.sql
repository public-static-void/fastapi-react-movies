PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE actors (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO actors VALUES(1,'Benicio del Toro');
INSERT INTO actors VALUES(2,'Brad Pitt');
INSERT INTO actors VALUES(3,'John Travolta');
INSERT INTO actors VALUES(4,'Samuel L. Jackson');
INSERT INTO actors VALUES(5,'Uma Thurman');
INSERT INTO actors VALUES(6,'Harvey Keitel');
INSERT INTO actors VALUES(7,'Bruce Willis');
INSERT INTO actors VALUES(8,'Robert De Niro');
INSERT INTO actors VALUES(9,'Ray Liotta');
INSERT INTO actors VALUES(10,'Joe Pesci');
INSERT INTO actors VALUES(11,'Tim Roth');
INSERT INTO actors VALUES(12,'Steve Buscemi');
INSERT INTO actors VALUES(13,'Al Pacino');
INSERT INTO actors VALUES(14,'Sharon Stone');
INSERT INTO actors VALUES(15,'Danny Glover');
INSERT INTO actors VALUES(16,'Tobin Bell');
INSERT INTO actors VALUES(17,'Marlon Brando');
INSERT INTO actors VALUES(18,'Robert Duvall');
INSERT INTO actors VALUES(19,'Diane Keaton');
CREATE TABLE categories (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO categories VALUES(1,'Crime');
INSERT INTO categories VALUES(2,'Horror');
INSERT INTO categories VALUES(3,'Drama');
INSERT INTO categories VALUES(4,'Comedy');
CREATE TABLE series (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	sort_name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	UNIQUE (sort_name)
);
INSERT INTO series VALUES(1,'Saw','saw');
INSERT INTO series VALUES(2,'The Godfather','godfather');
CREATE TABLE studios (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	sort_name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	UNIQUE (sort_name)
);
INSERT INTO studios VALUES(1,'Paramount Pictures','paramount pictures');
INSERT INTO studios VALUES(2,'Twisted Pictures','twisted pictures');
INSERT INTO studios VALUES(3,'Universal Pictures','universal pictures');
INSERT INTO studios VALUES(4,'Warner Bros.','warner bros');
INSERT INTO studios VALUES(5,'Miramax Films','miramax films');
INSERT INTO studios VALUES(6,'Sony Pictures','sony pictures');
CREATE TABLE movies (
	id INTEGER NOT NULL, 
	filename VARCHAR(255) NOT NULL, 
	name VARCHAR(255), 
	sort_name VARCHAR(255), 
	series_id INTEGER, 
	series_number INTEGER, 
	studio_id INTEGER, 
	processed BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (filename), 
	FOREIGN KEY(series_id) REFERENCES series (id), 
	FOREIGN KEY(studio_id) REFERENCES studios (id)
);
INSERT INTO movies VALUES(1,'[Universal Pictures] Casino (Joe Pesci, Robert De Niro, Sharon Stone).mp4','Casino','casino',NULL,NULL,3,1);
INSERT INTO movies VALUES(2,'[Warner Bros.] Goodfellas (Joe Pesci, Ray Liotta, Robert De Niro).mp4','Goodfellas','goodfellas',NULL,NULL,4,1);
INSERT INTO movies VALUES(3,'[Warner Bros.] Heat (Al Pacino, Robert De Niro).mp4','Heat','heat',NULL,NULL,4,1);
INSERT INTO movies VALUES(4,'[Miramax Films] Pulp Fiction (Bruce Willis, Harvey Keitel, John Travolta, Samuel L. Jackson, Tim Roth, Uma Thurman).mp4','Pulp Fiction','pulp fiction',NULL,NULL,5,1);
INSERT INTO movies VALUES(5,'[Miramax Films] Reservoir Dogs (Harvey Keitel, Steve Buscemi, Tim Roth).mp4','Reservoir Dogs','reservoir dogs',NULL,NULL,5,1);
INSERT INTO movies VALUES(6,'[Twisted Pictures] {Saw 2} Saw II (Tobin Bell).mp4','Saw II','saw ii',1,2,2,1);
INSERT INTO movies VALUES(7,'[Twisted Pictures] {Saw 3} Saw III (Tobin Bell).mp4','Saw III','saw iii',1,3,2,1);
INSERT INTO movies VALUES(8,'[Twisted Pictures] {Saw 1} Saw (Danny Glover).mp4','Saw','saw',1,1,2,1);
INSERT INTO movies VALUES(9,'[Sony Pictures] Snatch (Benicio del Toro, Brad Pitt).mp4','Snatch','snatch',NULL,NULL,6,1);
INSERT INTO movies VALUES(10,'[Paramount Pictures] {The Godfather 2} The Godfather Part II (Al Pacino, Diane Keaton, Robert De Niro, Robert Duvall).mp4','The Godfather Part II','godfather part ii',2,2,1,1);
INSERT INTO movies VALUES(11,'[Paramount Pictures] {The Godfather 3} The Godfather Part III (Al Pacino, Diane Keaton).mp4','The Godfather Part III','godfather part iii',2,3,1,1);
INSERT INTO movies VALUES(12,'[Paramount Pictures] {The Godfather 1} The Godfather (Al Pacino, Diane Keaton, Marlon Brando, Robert Duvall).mp4','The Godfather','godfather',2,1,1,1);
CREATE TABLE movie_actors (
	movie_id INTEGER NOT NULL, 
	actor_id INTEGER NOT NULL, 
	PRIMARY KEY (movie_id, actor_id), 
	FOREIGN KEY(movie_id) REFERENCES movies (id), 
	FOREIGN KEY(actor_id) REFERENCES actors (id)
);
INSERT INTO movie_actors VALUES(1,8);
INSERT INTO movie_actors VALUES(1,14);
INSERT INTO movie_actors VALUES(1,10);
INSERT INTO movie_actors VALUES(12,13);
INSERT INTO movie_actors VALUES(12,17);
INSERT INTO movie_actors VALUES(12,18);
INSERT INTO movie_actors VALUES(12,19);
INSERT INTO movie_actors VALUES(10,13);
INSERT INTO movie_actors VALUES(10,18);
INSERT INTO movie_actors VALUES(10,19);
INSERT INTO movie_actors VALUES(10,8);
INSERT INTO movie_actors VALUES(11,13);
INSERT INTO movie_actors VALUES(11,19);
INSERT INTO movie_actors VALUES(2,8);
INSERT INTO movie_actors VALUES(2,9);
INSERT INTO movie_actors VALUES(2,10);
INSERT INTO movie_actors VALUES(3,13);
INSERT INTO movie_actors VALUES(3,8);
INSERT INTO movie_actors VALUES(4,3);
INSERT INTO movie_actors VALUES(4,4);
INSERT INTO movie_actors VALUES(4,5);
INSERT INTO movie_actors VALUES(4,6);
INSERT INTO movie_actors VALUES(4,11);
INSERT INTO movie_actors VALUES(4,7);
INSERT INTO movie_actors VALUES(9,1);
INSERT INTO movie_actors VALUES(9,2);
INSERT INTO movie_actors VALUES(5,6);
INSERT INTO movie_actors VALUES(5,11);
INSERT INTO movie_actors VALUES(5,12);
INSERT INTO movie_actors VALUES(8,15);
INSERT INTO movie_actors VALUES(6,16);
INSERT INTO movie_actors VALUES(7,16);
CREATE TABLE movie_categories (
	movie_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	PRIMARY KEY (movie_id, category_id), 
	FOREIGN KEY(movie_id) REFERENCES movies (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id)
);
INSERT INTO movie_categories VALUES(1,1);
INSERT INTO movie_categories VALUES(1,3);
INSERT INTO movie_categories VALUES(12,1);
INSERT INTO movie_categories VALUES(12,3);
INSERT INTO movie_categories VALUES(10,1);
INSERT INTO movie_categories VALUES(10,3);
INSERT INTO movie_categories VALUES(11,1);
INSERT INTO movie_categories VALUES(11,3);
INSERT INTO movie_categories VALUES(2,1);
INSERT INTO movie_categories VALUES(2,3);
INSERT INTO movie_categories VALUES(3,1);
INSERT INTO movie_categories VALUES(3,3);
INSERT INTO movie_categories VALUES(4,4);
INSERT INTO movie_categories VALUES(4,1);
INSERT INTO movie_categories VALUES(9,1);
INSERT INTO movie_categories VALUES(9,4);
INSERT INTO movie_categories VALUES(5,1);
INSERT INTO movie_categories VALUES(5,3);
INSERT INTO movie_categories VALUES(8,2);
INSERT INTO movie_categories VALUES(6,2);
INSERT INTO movie_categories VALUES(7,2);
COMMIT;
