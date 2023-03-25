# import the neo4j driver for Python

from neo4j import GraphDatabase

 

# Database Credentials

uri             = "bolt://localhost:7687"

userName        = "neo4j"

password        = "9977"

 

# Connect to the neo4j database server

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))
# print(graphDB_Driver)

cqlNodeQuery = "MATCH (n:MyNode) RETURN n LIMIT 25"

# # Execute the CQL query

with graphDB_Driver.session() as graphDB_Session:

#     # Create nodes

#     # graphDB_Session.run(cqlCreate)

   

#     # Query the graph    

    nodes = graphDB_Session.run(cqlNodeQuery)

   

    print("List of Ivy League universities present in the graph:")

    # for node in nodes:

    #     print(node)