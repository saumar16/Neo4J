from unittest import result
import numpy as np
import random
import pandas as pd

import json

from neo4j import GraphDatabase



# transaction_execution_commands = []

# for i in transaction_list:
#     neo4j_create_statemenet = "create (t:Transaction {transaction_id:" + str(i[0]) +", vendor_number:  " + str(i[1]) +", transaction_amount: " + str(i[2]) +", transaction_type: '" + str(i[3]) + "'})"
#     transaction_execution_commands.append(neo4j_create_statemenet)

    
data_base_connection = GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", "9977"))
session = data_base_connection.session()    
nodes =session.run("MATCH (n:MyNode) RETURN n LIMIT 25")
# print(nodes.value()[0]._properties)
Data=[]
for node in nodes.value():
    Data.append(node._properties)
print(Data[0].values())


        
