# Name: Jai Gollapudi
# Class: DS4300
# Assignment: HW1

# Import necessary modules/APIs
from utils import DBUtils, TwitterAPI

# Database credentials
DB_HOST = ''  # Replace with your host
DB_USER = ''  # Replace with your user
DB_PASS = ''  # Replace with your password
DB_NAME = ''  # Replace with your DB

# Initializing DBUtils object with database credentials
# DBUtils will establish the database connection
db_utils = DBUtils(DB_HOST, DB_USER, DB_PASS, DB_NAME)

# Handling the case where the connection could not be established
if db_utils.connection is None:
    print("Failed to connect to the database. Please check your credentials.")
    exit(1)

# Initializing TwitterAPI object with DBUtils
# TwitterAPI provides a higher-level API for Twitter operations
twitter_api = TwitterAPI(db_utils)

