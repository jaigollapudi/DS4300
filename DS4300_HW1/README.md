# Twitter RDB Application Setup Guide

## Introduction
This guide provides instructions on how to set up and run the Twitter RDB application, which is designed to test the performance of a relational database system for handling tweets and user timelines.

## Prerequisites
- MySQL Database
- Python (version 3.9.13)

## Installation Steps

### 1. Database Setup
* Ensure MySQL is installed and running on your system. 
* Run the .sql file provided to load the database onto your local machine.

### 2. Environment Configuration
Input your credentials in 'main.py' for your database connection:
- `DB_HOST`: The host of your MySQL database.
- `DB_USER`: Your database username.
- `DB_PASS`: Your database password.
- `DB_NAME`: The name of your database (twitter_db in my case.)


### 3. Python Environment Setup
Install the required Python libraries:
```bash
pip install mysql-connector-python pandas
```

### 4. Data

- You can load the data in `follows.csv` into the FOLLOWS table programmatically or by using data import utilities.
- Ensure the `tweet.csv` file, which contains the tweet data, is placed in the project's root directory. The format of the CSV should match the expected input in the script (i.e., columns for user_id and tweet_text).

## Running the Application

### Performance Testing
To run the performance tests, execute the `test.py` script in the terminal:
```bash
python test.py
```
This may take anywhere from 500 - 600 seconds to run the whole test. 

- Test 1 will report tweets posted per second. (For 1 million tweets)
- Test 2 will report home timelines retrieved per second. It will also print the home timeline of 1 randomly selected user. (For 1000 home timelines)