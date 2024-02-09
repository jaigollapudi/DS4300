# Name: Jai Gollapudi
# Class: DS4300
# Assignment: HW1

# Import necessary modules
import mysql.connector
from mysql.connector import Error
import pandas as pd


class DBUtils:
    def __init__(self, host, user, password, database):
        """
        Initializes the DBUtils class and establishes a database connection.
        :param host: Hostname of the database server.
        :param user: Username for the database.
        :param password: Password for the database.
        :param database: Database name.
        """
        try:
            # Establishing a connection to the database
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("MySQL Database connection successful")
        except Error as e:
            # Handling any connection errors
            print(f"Error: '{e}'")
            self.connection = None

    def get_max_user_id(self):
        """
        Retrieves the maximum user ID from the TWEET table.
        This helps in determining the range of existing user IDs.
        :return: The maximum user ID present in the TWEET table.
        """
        try:
            # Querying the DB to retrieve the max user id in the TWEET table
            cursor = self.connection.cursor()
            query = "SELECT MAX(user_id) FROM TWEET"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except Error as e:
            # Handling any DB query errors
            print(f"Error: {e}")
            return 0

    def insert_tweet(self, user_id, tweet_text):
        """
        Inserts a tweet into the TWEET table.
        :param user_id: The ID of the user posting the tweet.
        :param tweet_text: The text content of the tweet.
        """
        try:
            # Querying the DB to insert tweets into the TWEET table
            cursor = self.connection.cursor()
            query = "INSERT INTO TWEET (user_id, tweet_text) VALUES (%s, %s)"
            cursor.execute(query, (user_id, tweet_text))
            self.connection.commit()
            cursor.close()
        except Error as e:
            # Handling any DB query errors
            print(f"Error: {e}")

    def fetch_home_timeline(self, user_id):
        """
        Retrieves the 10 most recent tweets from users followed by the given user
        by joining the TWEET and FOLLOWS tables and ordering by timestamp.
        :param user_id: The ID of the user whose home timeline is being requested.
        :return: A DataFrame containing the most recent tweets (User ID and Tweet Text).
        """
        try:
            # Querying the DB to fetch home timeline (10 tweets) for a given user id
            cursor = self.connection.cursor()
            query = """
            SELECT T.user_id, T.tweet_text
            FROM TWEET T
            JOIN FOLLOWS F ON T.user_id = F.follows_id
            WHERE F.user_id = %s
            ORDER BY T.tweet_ts DESC
            LIMIT 10
            """
            cursor.execute(query, (user_id,))
            timeline = cursor.fetchall()
            cursor.close()

            # Creating a DataFrame from the retrieved data
            df_timeline = pd.DataFrame(timeline, columns=['User ID', 'Tweet Text'])
            return df_timeline
        except Error as e:
            # Handling any DB query errors
            print(f"Error: {e}")
            # Returning an empty DataFrame in case of an error
            return pd.DataFrame()


class TwitterAPI:
    """
        This TwitterAPI class provides higher-level functions that abstract the database operations.
        It utilizes DBUtils for database interactions.
    """
    def __init__(self, db_utils):
        """
            Initializes the TwitterAPI with DBUtils object.
            :param db_utils: An instance of the DBUtils class for database operations.
        """
        self.db_utils = db_utils

    def get_max_user_id(self):
        """
        Retrieves the maximum user ID using DBUtils.
        :return: The maximum user ID.
        """
        return self.db_utils.get_max_user_id()

    def post_tweet(self, user_id, tweet_text):
        """
        Posts a tweet using DBUtils.
        :param user_id: The ID of the user posting the tweet.
        :param tweet_text: The text content of the tweet.
        """
        self.db_utils.insert_tweet(user_id, tweet_text)

    def get_home_timeline(self, user_id):
        """
        Gets the home timeline for a user using DBUtils.
        :param user_id: The ID of the user whose home timeline is being requested.
        :return: A DataFrame of the user's home timeline.
        """
        return self.db_utils.fetch_home_timeline(user_id)
