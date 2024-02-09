# Name: Jai Gollapudi
# Class: DS4300
# Assignment: HW2

# Import necessary modules/APIs
import csv
import time
import random
from main import twitter_api

def test_post_tweet_performance_s1(file_path):
    """
    Tests the performance of posting tweets using Strategy 1.

    :param file_path: Path to the CSV file containing tweets to post.
    """
    print("Testing Strategy 1: Posting Tweets Performance")
    # Recording the start time and initializing tweet counter
    start_time = time.time()
    tweet_count = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skipping the header row
        # Iterating over each row in the CSV file and extracting user ID and tweet text
        for row in csv_reader:
            user_id, tweet_text = row
            twitter_api.post_tweet_s1(int(user_id), tweet_text) # Posting the tweet
            tweet_count += 1
            if tweet_count % 10000 == 0:  # Printing progress every 10,000 tweets.
                print(f"S1: Posted {tweet_count} tweets...")
    # Printing the performance metrics
    print_performance_metrics("S1: Posting Tweets", tweet_count, start_time)

def test_get_home_timeline_performance_s1(num_iterations, max_user_id):
    """
    Tests the performance of fetching home timelines using Strategy 1.

    :param num_iterations: Number of home timelines to fetch for testing.
    :param max_user_id: The maximum user ID available in the system, to ensure random IDs are valid.
    """
    print(100*'-')
    print("Testing Strategy 1: Fetching Home Timelines Performance")
    test_timeline_performance("S1", num_iterations, max_user_id, twitter_api.get_home_timeline_s1)

def test_post_tweet_performance_s2(file_path):
    """
    Tests the performance of posting tweets using Strategy 2.

    :param file_path: Path to the CSV file with tweets to post.
    """
    print("Testing Strategy 2: Posting Tweets Performance")
    # Recording the start time and initializing tweet counter
    start_time = time.time()
    tweet_count = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skipping the header row
        # Iterating over each row in the CSV file and extracting user ID and tweet text
        for row in csv_reader:
            user_id, tweet_text = row
            twitter_api.post_tweet_s2(int(user_id), tweet_text) # Posting the tweet
            tweet_count += 1
            if tweet_count % 10000 == 0: # Printing progress every 10,000 tweets.
                print(f"S2: Posted {tweet_count} tweets...")
    # Printing the performance metrics
    print_performance_metrics("S2: Posting Tweets", tweet_count, start_time)

def test_get_home_timeline_performance_s2(num_iterations, max_user_id):
    """
    Tests the performance of fetching home timelines using Strategy 2.

    :param num_iterations: Number of iterations to perform the test.
    :param max_user_id: Maximum user ID in the system for generating valid random user IDs.
    """
    print("Testing Strategy 2: Fetching Home Timelines Performance")
    test_timeline_performance("S2", num_iterations, max_user_id, twitter_api.get_home_timeline_s2)

def print_performance_metrics(test_name, count, start_time):
    """
    Prints performance metrics for a test, including total API calls, duration, and operations per second.

    :param test_name: Name of the test for which metrics are being printed.
    :param count: Total number of API calls performed in the test.
    :param start_time: Timestamp when the test started.
    """
    duration = time.time() - start_time
    print(f"{test_name} - {count} API calls took {duration:.2f} seconds, {count / duration:.2f} API calls/second")
    print(100 * '-')

def test_timeline_performance(strategy, num_iterations, max_user_id, timeline_function):
    """
    Measures and prints performance metrics for fetching home timelines.

    :param strategy: Label indicating the strategy being tested ("S1" or "S2").
    :param num_iterations: Number of timelines to fetch for the test.
    :param max_user_id: Maximum user ID available to ensure generated IDs are valid.
    :param timeline_function: The function to call for fetching a timeline (corresponding to the strategy).
    """
    start_time = time.time() # Recording the start time
    # Performing the test for the specified number of iterations on a random user ID
    for _ in range(num_iterations):
        random_user_id = random.randint(1, max_user_id)
        timeline_function(random_user_id)
    print_performance_metrics(f"{strategy}: Fetching Home Timelines", num_iterations, start_time)


if __name__ == "__main__":
    tweets_file_path = "/Users/jaigollapudi/Downloads/hw1_data/tweet.csv"  # Change to your local file path if not in the same root directory
    follows_file_path = "/Users/jaigollapudi/Downloads/hw1_data/follows.csv"  # Change to your local file path if not in the same root directory

    # Load follower relationships into Redis before running the tests.
    twitter_api.redis_utils.load_followers(follows_file_path)

    # Dynamically get the max user ID from Redis
    max_user_id = twitter_api.get_max_user_id()

    # Run tests for Strategy 1
    test_post_tweet_performance_s1(tweets_file_path)
    test_get_home_timeline_performance_s1(2, max_user_id)

    # Run tests for Strategy 2
    test_post_tweet_performance_s2(tweets_file_path)
    test_get_home_timeline_performance_s2(1000, max_user_id)

    # Close the Redis connection
    twitter_api.redis_utils.connection.close()