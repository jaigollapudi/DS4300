-- Name: Jai Gollapudi
-- Class: DS4300
-- Assignment: HW1

-- Checking if the 'twitter_db' database exists and creating it if it doesn't
CREATE DATABASE IF NOT EXISTS `twitter_db`;
-- Using the 'twitter_db' database 
USE `twitter_db`;

-- Creating the 'TWEET' table to store tweets
CREATE TABLE TWEET (
    tweet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tweet_ts DATETIME DEFAULT CURRENT_TIMESTAMP,
    tweet_text VARCHAR(140),
    -- Using an index on 'user_id' for faster query performance when filtering by user
    INDEX(user_id)
);

-- Creating the 'FOLLOWS' table to store the follower relationships between users
CREATE TABLE FOLLOWS (
    user_id INT,
    follows_id INT,
    -- Using an index on 'user_id' for faster query performance when finding who a user follows
    INDEX(user_id),
    -- Using an index on 'follows_id' for faster query performance when finding who follows a user
    INDEX(follows_id)
);