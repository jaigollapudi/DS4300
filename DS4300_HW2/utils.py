# Name: Jai Gollapudi
# Class: DS4300
# Assignment: HW2

# Import necessary modules
import redis
import csv
import time
import datetime


class RedisUtils:
    """
    Handles direct interaction with the Redis database, implementing functionalities for posting tweets,
    fetching timelines, and managing user and follower data.
    """
    def __init__(self, host, port):
        """
        Initialize a Redis connection

        :param host: Hostname of the Redis server
        :param port: Port number for the Redis server
        """
        # Test connection
        try:
            self.connection = redis.Redis(host=host, port=port, decode_responses=True)
            self.connection.ping()
            print("Redis connection successful")
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")
            self.connection = None

    def load_followers(self, file_path):
        """
        Loads follower relationships from a CSV file into Redis.

        :param file_path: Path to the CSV file containing follower relationships.
        """
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skipping header row
            for row in csv_reader:
                user_id, follows_id = row
                # Adding each relationship to the corresponding Redis sets
                self.connection.sadd(f"followers:{follows_id}", user_id)
                self.connection.sadd("user_ids", user_id, follows_id)

    def get_max_user_id(self):
        """
        Retrieves the highest user ID from the stored user IDs in Redis.

        :return: The maximum user ID as an integer.
        """
        all_user_ids = self.connection.smembers("user_ids")
        # Validating if user_id provided is in digits format
        valid_user_ids = [user_id for user_id in all_user_ids if user_id.isdigit()]
        if not valid_user_ids:
            return 0
        max_user_id = max(map(int, valid_user_ids))
        return max_user_id

    # Strategy 1: Simple set operation for posting tweets, construct timeline on the fly
    def insert_tweet_s1(self, user_id, tweet_text):
        """
        Inserts a tweet using Strategy 1, where tweets are simply stored without immediate timeline updates.

        :param user_id: ID of the user posting the tweet.
        :param tweet_text: Text content of the tweet.
        """
        tweet_id = self.connection.incr("tweet_id_s1")
        tweet_data = f"{user_id}|{tweet_text}|{int(time.time())}"  # Simple serialization
        self.connection.set(f"tweet_s1:{tweet_id}", tweet_data)

    def fetch_home_timeline_s1(self, user_id):
        followers = self.connection.smembers(f"followers:{user_id}")
        all_tweets = []

        # Using SCAN to iterate over tweet keys more efficiently.
        cursor = '0'
        while cursor != 0:
            cursor, keys = self.connection.scan(cursor=cursor, match=f"tweet_s1:*", count=10)
            for tweet_key in keys:
                tweet_data = self.connection.get(tweet_key)
                if tweet_data:
                    tweet_user_id, tweet_text, timestamp = tweet_data.split("|")
                    if tweet_user_id in followers:
                        all_tweets.append({
                            'user_id': tweet_user_id,
                            'text': tweet_text,
                            'timestamp': datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
                        })

        # Sorting tweets by timestamp to get the 10 most recent tweets.
        ordered_tweets = sorted(all_tweets, key=lambda x: x['timestamp'], reverse=True)[:10]
        return ordered_tweets

    # Strategy 2: Post a tweet and update timelines immediately
    def insert_tweet_s2(self, user_id, tweet_text):
        """
        Inserts a tweet and updates followers' timelines immediately using Strategy 2.

        :param user_id: ID of the user posting the tweet.
        :param tweet_text: Text content of the tweet.
        """
        tweet_id = self.connection.incr("tweet_id_s2")
        self.connection.hset(f"tweet_s2:{tweet_id}", mapping={
            "user_id": user_id,
            "text": tweet_text,
            "timestamp": int(time.time())
        })
        # Adding tweet ID to the posting user's timeline and track user ID
        self.connection.lpush(f"timeline_s2:{user_id}", tweet_id)
        self.connection.sadd("user_ids_s2", user_id)

        # Adding tweet ID to followers' timelines
        followers = self.connection.smembers(f"followers_s2:{user_id}")
        for follower_id in followers:
            self.connection.lpush(f"timeline_s2:{follower_id}", tweet_id)

    # Strategy 2: Fetch the home timeline, including tweets from followed users and the user's own tweets
    def fetch_home_timeline_s2(self, user_id):
        tweet_ids = self.connection.lrange(f"timeline_s2:{user_id}", 0, 9)
        # Iterating over each tweet ID to fetch its details.
        tweets = [self.connection.hgetall(f"tweet_s2:{tweet_id}") for tweet_id in tweet_ids]

        ordered_tweets = []
        for tweet in tweets:
            readable_timestamp = datetime.datetime.fromtimestamp(int(tweet['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
            # Creating a dictionary with the formatted tweet details and add it to the list of tweets.
            ordered_tweet = {
                'user_id': tweet['user_id'],
                'text': tweet['text'],
                'timestamp': readable_timestamp
            }
            ordered_tweets.append(ordered_tweet)

        return ordered_tweets


class TwitterAPI:
    """
    Provides a high-level API for Twitter-like operations, abstracting away the direct Redis interactions.
    """
    def __init__(self, redis_utils):
        """
        Initializes the TwitterAPI with a RedisUtils object.
        :param redis_utils: An instance of the RedisUtils class for database operations.
        """
        self.redis_utils = redis_utils


    def get_max_user_id(self):
        """
        Wrapper method to retrieve the maximum user ID stored in Redis.

        :return: The highest user ID as an integer.
        """
        return self.redis_utils.get_max_user_id()

    # Strategy 1 API Methods
    def post_tweet_s1(self, user_id, tweet_text):
        """
        Posts a tweet using Strategy 1.
        :param user_id: The ID of the user posting the tweet.
        :param tweet_text: The text content of the tweet.
        """
        self.redis_utils.insert_tweet_s1(user_id, tweet_text)

    def get_home_timeline_s1(self, user_id):
        """
        Gets the home timeline for a user using Strategy 1.
        :param user_id: The ID of the user whose home timeline is being requested.
        :return: A list of the user's home timeline tweets.
        """
        return self.redis_utils.fetch_home_timeline_s1(user_id)

    # Strategy 2 API Methods
    def post_tweet_s2(self, user_id, tweet_text):
        """
        Posts a tweet using Strategy 2.
        :param user_id: The ID of the user posting the tweet.
        :param tweet_text: The text content of the tweet.
        """
        self.redis_utils.insert_tweet_s2(user_id, tweet_text)

    def get_home_timeline_s2(self, user_id):
        """
        Gets the home timeline for a user using Strategy 2.
        :param user_id: The ID of the user whose home timeline is being requested.
        :return: A list of the user's home timeline tweets.
        """
        return self.redis_utils.fetch_home_timeline_s2(user_id)
