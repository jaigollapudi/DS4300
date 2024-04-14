import pandas as pd
from scipy.spatial.distance import cdist

class SongRecommender:
    """
    A class to recommend songs based on similarity to a given set of songs.
    This implementation uses musical features to determine similarity and
    generates recommendations excluding specific artists and their songs.

    :param data_path (str): The path to the dataset file.
    :param df (DataFrame): The loaded dataset.
    :param final_sample (DataFrame): The filtered and sampled dataset.
    :param distance_df (DataFrame): A DataFrame containing distance metrics between songs.
    :param top_similar_songs_df (DataFrame): The top N similar songs for each song in the dataset.
    :param features (list): The list of song features to use for similarity calculation.
    """

    def __init__(self, data_path):
        """
        Initializes the SongRecommender with a dataset path.

        :param data_path (str): The path to the dataset file.
        """
        self.data_path = data_path
        self.df = None
        self.final_sample = None
        self.distance_df = None
        self.top_similar_songs_df = None
        self.features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                         'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                         'time_signature']

    def load_data(self):
        """
        Loads the dataset from the specified data path into a DataFrame.
        """
        self.df = pd.read_csv(self.data_path)

    def filter_and_sample_data(self, artist_name, album_name, sample_size=10000):
        """
        Filters out songs by a specific artist and album, then samples the dataset to manage size.
        The sampling now considers the genre of the target album to recommend songs within the same genre.

        :param artist_name (str): The name of the artist to filter by.
        :param album_name (str): The name of the album to filter by.
        :param sample_size (int): The number of songs to sample from the dataset.
        """
        # Finding the genre(s) of the target album
        target_genres = self.df[
            (self.df['artists'] == artist_name) &
            (self.df['album_name'] == album_name)
            ]['track_genre'].unique()

        # Getting all songs from the target album
        target_songs = self.df[
            (self.df['artists'] == artist_name) &
            (self.df['album_name'] == album_name)
            ]

        # Filtering the dataset to exclude songs from the target album
        df_excluding_target = self.df[
            ~((self.df['artists'] == artist_name) &
              (self.df['album_name'] == album_name))
        ]

        # Filtering by genre and make sure there are enough songs to sample
        genre_filtered_songs = df_excluding_target[
            df_excluding_target['track_genre'].isin(target_genres)
        ]

        # Adjusting sample size if it's larger than the available songs
        actual_sample_size = min(sample_size, len(genre_filtered_songs))

        # Sampling other songs, considering only those that match the genre(s) of the target album
        sampled_songs = genre_filtered_songs.sample(n=actual_sample_size, random_state=1)

        # Combining the target songs with the sampled songs
        self.final_sample = pd.concat([target_songs, sampled_songs]).drop_duplicates()
        self.final_sample.to_csv('sampled_songs_genre_filtered.csv', index=False)

    def normalize_features(self):
        """
        Normalizes the feature values in the final sample dataset.
        """
        for feature in self.features:
            # Normalizing features
            self.final_sample[feature] = (self.final_sample[feature] - self.final_sample[feature].min()) / (
                        self.final_sample[feature].max() - self.final_sample[feature].min())

    def calculate_distances(self):
        """
        Calculates the Euclidean distance between each pair of songs based on their features.
        The results are stored in a distance DataFrame.
        """
        features_df = self.final_sample[self.features]
        # Calculating the distance between songs based on selected features
        self.distance_matrix = cdist(features_df, features_df, metric='euclidean')
        self.distance_df = pd.DataFrame(self.distance_matrix, index=self.final_sample.index,
                                        columns=self.final_sample.index)

    def rank_similarities(self, N=5):
        """
        Ranks songs based on their similarity to each other, keeping only the top N similar songs.

        :param N (int): The number of top similar songs to keep for each song.
        """
        top_similar_songs = []

        for index, row in self.distance_df.iterrows():
            # Getting the sorted distances but skip the first one (distance to itself)
            sorted_distances = row.sort_values().iloc[1:]
            # Getting the track_id for the current song
            track_id_1 = self.final_sample.loc[self.final_sample.index == index, 'track_id'].values[0]

            rank = 1
            for track_id_2_index, distance in sorted_distances.items():
                if rank > N:  # Only considering the top N similar songs
                    break

                # Getting the track_id for the similar song
                track_id_2 = self.final_sample.loc[self.final_sample.index == track_id_2_index, 'track_id'].values[0]

                # Checking that I'm not looking at the same song and the distance is greater than zero
                if track_id_1 != track_id_2 and distance > 0:
                    top_similar_songs.append([track_id_1, track_id_2, rank, distance])
                    rank += 1  # Only incrementing rank if the song is valid

        # Creating a DataFrame from the list
        self.top_similar_songs_df = pd.DataFrame(top_similar_songs, columns=['track_id_1', 'track_id_2', 'rank', 'distance'])

        # Saving the DataFrame to a CSV file
        self.top_similar_songs_df.to_csv('top_similar_songs.csv', index=False)

    def run(self):
        """
        Executes the recommendation process and returns the distance DataFrame.
        """
        self.load_data()
        self.filter_and_sample_data()
        self.normalize_features()
        self.calculate_distances()
        self.rank_similarities(N=5)
        return self.distance_df


# Implementation
recommender = SongRecommender('spotify.csv')
recommender.load_data()
recommender.filter_and_sample_data('The Strokes', 'Is This It')
recommender.normalize_features()
recommender.calculate_distances()
distance_df = recommender.rank_similarities(N=5)
print(distance_df)

