from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import datetime
from time import gmtime, strftime, mktime
import os, io, sys

import dao
from clean_graph import clean_and_dump
from distance import find_dist_and_dump, find_all_dist_and_dump

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://matron:<password>@matron-db-pxltz.azure.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)

dao = None

@app.route('/')
def index():
    return '<h1>Hello!</h1>'

# used to acquire the appropriate blue_print for a
# specific wing of a specific floor
@app.route('/blueprint/<string:name>', methods=['GET', 'POST'])
def blueprint(name):
    """
    fetches a saved blueprint, or saves a new blueprint into the
    database depending on the request type
    """
    if request.method == 'POST':
        img = request.files['image']
        return dao.save_blueprint(name, img)
    elif request.method == 'GET':
        return dao.get_blueprint(name)
    else:
        print("Invalid request type!")
        return jsonify({'status': 400})


@app.route('/graph/<string:name>', methods=['GET', 'POST', 'DELETE'])
def graph(name):
    """ 
    fetches a saved graph or save a new graph into the database
    depending on the request type

    name: the name of the graph
    """
    if request.method == 'POST':
        g = request.get_json()
        time = mktime(gmtime(0))
        graph = { "time" : time, "graph" : g}
        return dao.save_graph(name, jsonify(graph))
    elif request.method == 'GET':
        return dao.get_latest(name)
    elif request.method == 'DELETE':
        return delete_graph(name)
    else:
        print("Invalid request type!")  


@app.route('/graph/<string:name>/requestAll')
def get_all_versions(name):
    """ 
    acquires the 10 most recent dates of saves for a particular graph
    
    name: name of the graph to retrieve 
    """
    times = []

    graphs = dao.get_all_versions(name)
    for graph in graphs:
        times.append(strftime("%d %m %Y %H: %M: %S", gmtime(graph["time"])))
    return jsonify(times)


@app.route('/graph/<string:name>/<date>', methods=['GET', 'DELETE'])
def graph_version(name, date):
    """
    retrieves/deletes the specified version dates of a given graph

    name: name of the graph
    date: the version date wanted
    """
    utc_time = datetime.strptime(date, "%d %m %Y %H: %M: %S")
    epoch = timegm(utc_time)
    if request.method == 'GET':
        return dao.get_version(name, epoch)
    elif request.metohd == 'DELETE':
        return dao.delete_version(name, epoch)
    else:
        print("Error retreiving graph version: ", name," ", date)
        return jsonify({'status': 400})
        

@app.route('/graph/<string:graph_name>/<string:room>')
def distances_from_room(graph_name, room):
    """
    retrieves all distances of a specific room to the rest
    of the hospital wing

    graph_name: the name of the graph
    room:       the name of the room
    """
    graph = request.get_json()
    return find_dist_and_dump(graph, room)


@app.route('/graph/<string:graph_name>/distances')
def all_distances(graph_name):
    """
    retrieves every single distance from every room 
    from all rooms for a given hospital wing

    graph_name: name of the graph to be inspected
    """
    graph = request.get_json()
    return find_all_dist_and_dump(graph)


# TODO calculate distance between 2 specific rooms
@app.route('/graph/<string:graph_name>/<string:room_name0>/<string:room_name1>')
def retrieve_distance(graph_name, room_name0, room_name1):
    raise NotImplementedError


if __name__ == '__main__':
    dao = MongoDAO("matron", "<password>")
