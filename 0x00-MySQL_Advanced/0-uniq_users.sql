-- A sql script that createa table with the following columns
-- id, email, and name
CREATE TABLE IF NOT EXISTS users (
	id int NOT  NULL PRIMARY KEY AUTO_INCREMENT,
	email varchar(255) NOT NULL UNIQUE,
	name varchar(255));
