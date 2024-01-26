# CREATE DATABASE AND SET AS ACTIVE
CREATE DATABASE mydatabase;
USE mydatabase;


# CREATE TABLE AND COLUMNS
CREATE TABLE dictionary (
	words_ID int NOT NULL AUTO_INCREMENT,
    italy_word varchar(255),
    english_word varchar(255),
    PRIMARY KEY (words_ID)
);

# IF SOMETHING WRONG
DROP TABLE dictionary;

# TO CHECK HOW IT LOOKS
SELECT * FROM dictionary