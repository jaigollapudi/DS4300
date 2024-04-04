# Name: Jai Gollapudi
# Class: DS4300
# Assignment: HW4

# Importing packages
from hw4_api import GraphAPI

if __name__ == "__main__":

    graph_api = GraphAPI()

    # Flush the Redis database to start fresh
    graph_api.flush_db()

    # Adding nodes
    graph_api.add_node('Emily', 'Person')
    graph_api.add_node('Spencer', 'Person')
    graph_api.add_node('Brendan', 'Person')
    graph_api.add_node('Trevor', 'Person')
    graph_api.add_node('Paxton', 'Person')
    graph_api.add_node('Cosmos', 'Book')
    graph_api.add_node('Database Design', 'Book')
    graph_api.add_node('The Life of Cronkite', 'Book')
    graph_api.add_node('DNA and You', 'Book')

    # Adding edges
    graph_api.add_edge('Emily', 'Database Design', 'bought')
    graph_api.add_edge('Spencer', 'Cosmos', 'bought')
    graph_api.add_edge('Spencer', 'Database Design', 'bought')
    graph_api.add_edge('Brendan', 'Database Design', 'bought')
    graph_api.add_edge('Brendan', 'DNA and You', 'bought')
    graph_api.add_edge('Trevor', 'Cosmos', 'bought')
    graph_api.add_edge('Trevor', 'Database Design', 'bought')
    graph_api.add_edge('Paxton', 'Database Design', 'bought')
    graph_api.add_edge('Paxton', 'The Life of Cronkite', 'bought')
    graph_api.add_edge('Emily', 'Spencer', 'knows')
    graph_api.add_edge('Spencer', 'Brendan', 'knows')

    # Get recommendations for a specific person
    name = "Spencer"  # For demonstration, directly using 'Spencer'
    recommendations = graph_api.get_recommendations(name)
    print(f'Recommendations for {name}: {recommendations}')

    # Close the Redis connection at the end
    graph_api.close_connection()

