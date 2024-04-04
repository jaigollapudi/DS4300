# Name: Jai Gollapudi
# Class: DS4300
# Assignment: HW4

# Importing libraries
import redis

class GraphAPI:
    def __init__(self, host='localhost', port=6379, db=0):
        """Initialize the Redis connection."""
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def flush_db(self):
        """Flushes the Redis database to ensure a clean state."""
        self.redis_client.flushdb()

    def close_connection(self):
        """Closes the Redis connection."""
        self.redis_client.close()

    def add_node(self, name, type):
        """Add a node with a given name and type to the database.

        :param name: The name of the node to be added.
        :param type: The type of the node ('Person', 'Book').
        """
        self.redis_client.hset(f"node:{name}", "type", type)

    def add_edge(self, name1, name2, type):
        """Add an edge between two nodes with a specific type.

        :param name1: The name of the first node.
        :param name2: The name of the second node.
        :param type: The type of the edge ('knows', 'bought').
        """
        self.redis_client.sadd(f"edge:{name1}:{type}", name2)
        self.redis_client.sadd(f"edge:{name2}:{type}", name1)  # Assuming bidirectional relationship for simplicity

    def get_adjacent(self, name, node_type=None, edge_type=None):
        """Get the names of all adjacent nodes, optionally filtering by node or edge type.

        :param name: The name of the node for which to find adjacent nodes.
        :param node_type: Optional. The type of adjacent nodes to return (e.g., 'Book').
        :param edge_type: Optional. The type of edges to consider (e.g., 'bought').
        :return: A list of names of adjacent nodes matching the criteria.
        """
        adjacent_nodes = []
        if edge_type:
            adjacent_nodes = self.redis_client.smembers(f"edge:{name}:{edge_type}")
        else:
            # Fetching all edges if no edge_type is specified
            keys = self.redis_client.keys(f"edge:{name}:*")
            for key in keys:
                adjacent_nodes += list(self.redis_client.smembers(key))

        if node_type:
            # Filtering nodes by the specified type
            adjacent_nodes = [node for node in adjacent_nodes if self.redis_client.hget(f"node:{node}", "type") == node_type]

        return adjacent_nodes

    def get_recommendations(self, name):
        """Get book recommendations for a given person based on books purchased by the people they know.

        :param name: The name of the person for whom to get recommendations.
        :return: A list of book names recommended for the person.
        """
        friends = self.get_adjacent(name, edge_type='knows')
        recommended_books = set()
        for friend in friends:
            friend_books = set(self.get_adjacent(friend, node_type='Book', edge_type='bought'))
            user_books = set(self.get_adjacent(name, node_type='Book', edge_type='bought'))
            recommended_books |= friend_books - user_books
        return list(recommended_books)

