from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
import os

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = os.getenv('MONGO_DB_NAME','donorsUSA')
MONGO_URI = os.getenv('MONGODB_URI')
COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME','projects')
FIELDS = {'funding_status': True, 'school_state': True, 'resource_type': True, 'poverty_level': True,
          'date_posted': True, 'total_donations': True, '_id': False}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/donorsUS/projects")
def donor_projects():
    # connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    connection = MongoClient(MONGO_URI)
    # This connection is required when hosted using a remote mongo db.
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS, limit=55000)
    json_projects = list(projects)
    json_projects = json.dumps(json_projects)
    connection.close()
    return json_projects


if __name__ == "__main__":
    app.run(debug=True)
