from typing import Dict
from flask import Flask, Response, request, render_template, jsonify
import json
import re
from bson.objectid import ObjectId
import numpy as np
import random
import pandas as pd
from neo4j import GraphDatabase


app=Flask(__name__)


try:
    data_base_connection = GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", "9977"))
    session = data_base_connection.session() 
except:
    print("Error occured while connecting to neo4j database!!")


#   Requirement-1 Insert the new movie and show
@app.route('/api', methods=['POST'])
# user defined function to insert a new record and display
def insert_record():
  try:
      # getting user iput in json format
      recorddata = request.get_json()
    #   print(recorddata["title"])
      dbResponse = session.run("create (n:MyNode{id:'"+recorddata["id"]+"' , title: '"+recorddata["title"]+"', description: '"+recorddata["description"]+"', type: '"+recorddata["type"]+"', release_year: '"+recorddata["release_year"]+"', age_certification: '"+recorddata["age_certification"]+"', runtime: '"+recorddata["runtime"]+"', genres: "+recorddata["genres"]+", production_countries: '"+recorddata["production_countries"]+"', imdb_score: '"+recorddata["imdb_score"]+"'})")
      nodes =session.run("MATCH (n:MyNode) RETURN n")
        # print(nodes.value()[0]._properties)
      Data=[]
      for node in nodes.value():
        Data.append(node._properties)
      response = Response(json.dumps({ "Response":"Successfully inserted a new record in database!!", "Inserted Record":f"{Data}"}),status=201,mimetype='application/json')
      return response
  except Exception as exp:
      response = Response("Error occured while inserting new record!!",status=500,mimetype='application/json')
      return response


#	Requirement-2 Update the record using title. (By update only title, description and imdb score)
@app.route('/api/<string:title>', methods=['PATCH'])
def update_record_by_title(title):
    try:
        recorddata = request.get_json()
        getdbrecord1 = session.run("MATCH (n:MyNode) where n.title='"+title+"' RETURN n")
        if getdbrecord1:
            # for record in getdbrecord1:
            dbResponse = session.run("MATCH (n:MyNode) where n.title='"+title+"' set n.title="+recorddata["title"]+",n.description="+recorddata["description"]+",n.imdb_score="+recorddata["imdb_score"]+" RETURN n")
            Data=[]
            for node in dbResponse.value():
                Data.append(node._properties)
            return jsonify({ "Response":"Successfully updated the record in database!!", "Updated Record":f"{Data}"})
        else:
            response = Response("Record Not Found with given title!!",status=500,mimetype='application/json')
            return response
    except Exception as exp:
        response = Response("Error occured while updating the record!!",status=500,mimetype='application/json')
        return response


#   Requirement-3 Delete the record using title
@app.route('/api/<string:title>', methods=['DELETE'])
def delete_record_by_title(title):
    try:
        getdbrecord = session.run("MATCH (n:MyNode) where n.title='"+title+"' RETURN n")
        if getdbrecord:
            Data=[]
            for node in getdbrecord.value():
                Data.append(node._properties)
            dbResponse = session.run("MATCH (n:MyNode) where n.title='"+title+"' DELETE n")  
            response = Response(json.dumps({ "Response":"Successfully deleted the record in database!!", "Deleted Record":f"{Data}"}),status=200,mimetype='application/json')
            return response
        else:
            response = Response("Record Not Found with given title!!",status=500,mimetype='application/json')
            return response
    except Exception as exp:
        response = Response("Error occured while deleting the record!!",status=500,mimetype='application/json')
        return response


#   Requirement-4 Retrieve all the records of movies and shows in database
@app.route('/api', methods=['GET'])
def get_all_records():
    try:
        nodes =session.run("MATCH (n:MyNode) RETURN n")
        # print(nodes.value()[0]._properties)
        Data=[]
        for node in nodes.value():
            Data.append(node._properties)
        print(Data[0])
        return Response(json.dumps(Data),status = 200,mimetype =("application/json"))
    except Exception as exp:
        response = Response("Error occured while fetching and displaying the records!!",status=500,mimetype='application/json')
        return response

#	Requirement-5 Display the movie and show’s detail using title
@app.route('/api/<string:title>', methods=['GET'])
def search_record_by_title(title):
    try:
        getdbrecord = session.run("MATCH (n:MyNode) where n.title='"+title+"' RETURN n")
        if getdbrecord:
            Data=[]
            for node in getdbrecord.value():
                Data.append(node._properties)
            return jsonify(Data)
        else:
            response = Response("Record Not Found with given title!!",status=500,mimetype='application/json')
            return response
    except Exception as exp:
        response = Response("Error occured while fetching and displaying the record with given title!!",status=500,mimetype='application/json')
        return response



if __name__ == '__main__':
    app.run(port=3456, debug=True)