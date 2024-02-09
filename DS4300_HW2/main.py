# Name: Jai Gollapudi
# Class: DS4300
# Assignment: HW2

# Importing necessary modules/APIs
from utils import RedisUtils, TwitterAPI

# Redis credentials
DB_HOST = 'localhost'  # Replace with your host (str, ex: 'localhost')
DB_PORT = 6379  # Replace with your port (int, ex: 6379)

# Initializing RedisUtils object with Redis server credentials.
# This object handles direct interactions with Redis, including posting tweets and fetching timelines.
redis_utils = RedisUtils(DB_HOST, DB_PORT)

# Checking if the connection to Redis was successfully established.
# If not, printing an error message and exit the application to prevent further execution
if redis_utils.connection is None:
    print("Failed to connect to the database. Please check your credentials.")
    exit(1)

# Initializing TwitterAPI object with RedisUtils
# TwitterAPI provides a higher-level API for Twitter operations
twitter_api = TwitterAPI(redis_utils)

