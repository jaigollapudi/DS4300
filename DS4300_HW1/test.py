# Name: Jai Gollapudi
# Class: DS4300
# Assignment: HW1

# Import necessary modules/APIs
import csv
import time
import random
from main import twitter_api

def test_post_tweet_performance(file_path):
    """
        Tests the performance of posting tweets to the database,
        Reads tweets from a CSV file and posts them one by one,
        Measures the time taken to post a specified number of tweets.
        :param file_path: Path to the CSV file containing tweets.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # Skipping the header row if there is one
        next(csv_reader)

        # Starting the timer and setting tweet count to zero
        start_time = time.time()
        tweet_count = 0

        # Reading and posting each tweet from the CSV file
        for row in csv_reader:
            user_id, tweet_text = row  # Given the CSV has two columns: user_id and tweet_text
            twitter_api.post_tweet(user_id=int(user_id), tweet_text=tweet_text)
            tweet_count += 1

            # Printing progress every 10,000 tweets
            if tweet_count % 10000 == 0:
                print(f"Posted {tweet_count} tweets...")

    # Ending the timer
    end_time = time.time()

    # Computing tweets posted per second
    tweets_per_second = tweet_count/(end_time - start_time)
    print(f"Posting {tweet_count} tweets took {end_time - start_time} seconds")
    print(f"Tweets posted per second = {tweets_per_second}")


def test_get_home_timeline_performance(num_iterations, max_user_id):
    # Starting the timer
    start_time = time.time()

    # Fetching timelines for "num_iterations" users (num_iterations = how many users' timelines we're fetching for)
    for _ in range(num_iterations):
        random_user_id = random.randint(1, max_user_id)
        twitter_api.get_home_timeline(user_id=random_user_id)

    # Ending timer and computing timelines retrieved per second
    end_time = time.time()
    total_time = end_time - start_time
    timelines_per_second = num_iterations / total_time

    print(f"Retrieved {num_iterations} home timelines in {total_time} seconds")
    print(f"Home timelines retrieved per second: {timelines_per_second}")

    # Printing the timeline of the first random user for verification
    example_user_id = random.randint(1, max_user_id)
    example_timeline_df = twitter_api.get_home_timeline(user_id=example_user_id)
    print(f"Example timeline for user {example_user_id}:\n{example_timeline_df}")


if __name__ == "__main__":
    tweets_file_path = "tweet.csv"  # Change to your local file path if not in the same root directory

    # Testing post tweet performance
    # Comment the following line if you don't need to run the tweet posting test again
    test_post_tweet_performance(tweets_file_path)

    # Dynamically get the max user ID from the database
    max_user_id = twitter_api.get_max_user_id()
    num_iterations = 1000  # Number of users' home timeline retrievals to test

    # Testing get home timeline performance
    test_get_home_timeline_performance(num_iterations, max_user_id)
