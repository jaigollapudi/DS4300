# Twitter Redis Application Setup Guide

## Introduction
This guide provides instructions on how to set up and run the Twitter Redis application, which is designed to test the performance of Redis as a NoSQL database system for handling tweets and user timelines through two distinct strategies.

## Prerequisites
- Redis server
- Python (version 3.9.13 or compatible)

## Installation Steps

### 1. Redis Server Setup
* Ensure Redis is installed and running on your system. 
* You can start the Redis server by running `redis-server` in your terminal.

### 2. Environment Configuration
Configure the Redis connection in 'main.py' with the following details:
- `DB_HOST`: The hostname where your Redis server is running (usually `localhost`).
- `DB_PORT`: The port number on which your Redis server is listening (default is `6379`).

### 3. Python Environment Setup
Install the required Python libraries, including the Redis client for Python:
```bash
pip install redis 
```

Also ensure csv, time, random, and datetime are also installed in your environment.

### 4. Data

- Place the follows.csv file, which contains user follow relationships, in the project's root directory.
- Ensure the tweets.csv file, containing the tweet data, is also located in the project's root directory. 

## Running the Application

### Performance Testing
To run the performance tests for both Strategy 1 (S1) and Strategy 2 (S2), execute the test.py script in the terminal:
```bash
python test.py
```
Depending on the chosen strategy and number of iterations, the runtime may vary significantly.

For Strategy 1 (S1):
- Test 1 will measure and report the speed of posting tweets.
- Test 2 will evaluate the performance of fetching home timelines and might take longer due to the on-the-fly construction of timelines.

For Strategy 2 (S2):
- Test 1 will again report on the speed of posting tweets, similar to S1 but might show different performance characteristics due to immediate timeline updates.
- Test 2 will measure the efficiency of retrieving pre-computed home timelines, expected to be significantly faster than S1.

The tests will provide insights into the trade-offs between computational overhead at the time of posting tweets and the speed of timeline retrieval for each strategy.

### NOTE: Since the performance of S1 is extremely slow, I have limited it to 2 iterations.