CREATE TABLE IF NOT EXISTS movies (
	ID SERIAL PRIMARY KEY,
	movie VARCHAR(40),
	year INT,
	rating INT
);

SELECT * FROM movies;