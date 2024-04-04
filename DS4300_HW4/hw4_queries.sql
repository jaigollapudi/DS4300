-- Name: Jai Gollapudi
-- Class: DS4300
-- Assignment: HW4

USE graph;

-- a. What is the sum of all book prices? Give just the sum.


SELECT SUM(num_value) AS sum_book_prices
FROM node_props
WHERE propkey = 'price';

-- Output:
-- sum_book_prices
-- '253.45'

-- b. Who does spencer know? Give just their names.

SELECT np.string_value AS name
FROM node_props np
JOIN edge e ON np.node_id = e.out_node
JOIN node_props np2 ON e.in_node = np2.node_id
WHERE np.propkey = 'name' AND e.type = 'knows' AND np2.string_value = 'Spencer';

-- Output: 
-- name
-- 'Brendan'
-- 'Emily'

-- c. What books did Spencer buy? Give title and price.

SELECT np.string_value AS title, np2.num_value AS price
FROM node n
-- Joining with edges where the node is the destination (bought by someone).
JOIN edge e ON n.node_id = e.out_node
-- Joining with node_props to get the book title.
JOIN node_props np ON n.node_id = np.node_id AND np.propkey = 'title'
-- Joining again with node_props to get the book price.
JOIN node_props np2 ON n.node_id = np2.node_id AND np2.propkey = 'price'
-- Joining one more time with node_props to ensure the buyer is Spencer.
JOIN node_props np3 ON e.in_node = np3.node_id
WHERE n.type = 'Book' AND e.type = 'bought' AND np3.string_value = 'Spencer';

-- Output: 
-- title, price
-- 'Database Design', '195'
-- 'Cosmos', '17'

-- d. Who knows each other? Give just a pair of names.

-- I'm assuming that if person1 knows person 2 and person2 knows person1, its a mutual relationship (both know eachother).
-- Therefore, I will only be outputting a uni-directional relationship where person1 knows person2 as
-- it better represents the logic of relationships in my graph.

-- Selecting pairs of individuals who know each other, ensuring no duplicate reverse pairs.
-- First, selecting one direction of the "knows" relationship.
SELECT np1.string_value AS person1, np2.string_value AS person2
FROM edge e
JOIN node_props np1 ON e.in_node = np1.node_id AND np1.propkey = 'name'
JOIN node_props np2 ON e.out_node = np2.node_id AND np2.propkey = 'name'
WHERE e.type = 'knows' AND e.in_node < e.out_node
UNION
-- Then, selecting the reverse direction to ensure all pairs are captured.
SELECT np3.string_value AS person1, np4.string_value AS person2
FROM edge e
JOIN node_props np3 ON e.out_node = np3.node_id AND np3.propkey = 'name'
JOIN node_props np4 ON e.in_node = np4.node_id AND np4.propkey = 'name'
WHERE e.type = 'knows' AND e.out_node < e.in_node
ORDER BY person1, person2;

-- Output: 
-- person1, person2
-- 'Emily', 'Spencer'
-- 'Spencer', 'Brendan'



-- e. Demonstrate a simple recommendation engine by answering the following question with a SQL query: 
-- What books were purchased by people who Spencer knows? Exclude books that Spencer already owns. 

-- Selecting distinct titles and prices of books bought by people Spencer knows, excluding books Spencer already owns.
SELECT DISTINCT np.string_value AS title, np_price.num_value AS price
FROM edge e_knows
-- Joining to identify connections from Spencer to others.
JOIN node_props np_spencer ON e_knows.in_node = np_spencer.node_id AND np_spencer.string_value = 'Spencer'
-- Joining to find books bought by those Spencer knows.
JOIN edge e_bought ON e_knows.out_node = e_bought.in_node AND e_bought.type = 'bought'
-- Joining to get the title of the books bought.
JOIN node_props np ON e_bought.out_node = np.node_id AND np.propkey = 'title'
-- Joining to get the price of the books bought.
JOIN node_props np_price ON e_bought.out_node = np_price.node_id AND np_price.propkey = 'price'
-- Ensuring we exclude books that Spencer has already bought.
WHERE NOT EXISTS (
    SELECT 1
    FROM edge e_spencer_bought
    JOIN node_props np_spencer2 ON e_spencer_bought.in_node = np_spencer2.node_id AND np_spencer2.string_value = 'Spencer'
    WHERE e_spencer_bought.out_node = e_bought.out_node AND e_spencer_bought.type = 'bought'
)
AND e_knows.type = 'knows';

-- Output:
-- # title, price
-- 'DNA and you', '11.5'