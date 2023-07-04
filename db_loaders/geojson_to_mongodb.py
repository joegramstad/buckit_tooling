import json
from datetime import datetime
from pymongo import MongoClient, GEOSPHERE
from pymongo.errors import (PyMongoError, BulkWriteError)

input_file = 'geojson/USA_Counties.geojson'
uri = 'mongodb+srv://gramstad:1991JGoe@cluster0.x4k9zhn.mongodb.net/test'

with open(input_file, 'r') as f:
    geojson = json.loads(f.read())

client = MongoClient(uri)
db = client['United_States']
collection = db['US_Counties']

# create 2dsphere index and initialize unordered bulk insert
collection.create_index([("geometry", GEOSPHERE)])
bulk = collection.initialize_unordered_bulk_op()

for feature in geojson['features']:
    # Note: comment out next two lines if input file does not contain timestamp field having proper format
    # timestamp = feature['properties']['timestamp']
    # feature['properties']['timestamp'] = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    feature['name'] = feature['properties']['Name']
    feature['state'] = feature['properties']['State']
    feature['GlobalID'] = feature['properties']['GlobalID']
    del feature['properties']
    del feature['type']
    del feature['id']

    # append to bulk insert list
    bulk.insert(feature)

# execute bulk operation to the DB
try:
    result = bulk.execute()
    print("Number of Features successfully inserted:", result["nInserted"])
except BulkWriteError as bwe:
    nInserted = bwe.details["nInserted"]
    errMsg = bwe.details["writeErrors"]
    print("Errors encountered inserting features")
    print("Number of Features successfully inserted:", nInserted)
    print("The following errors were found:")
    for item in errMsg:
        print("Index of feature:", item["index"])
        print("Error code:", item["code"])
        print("Message (truncated due to data length):", item["errmsg"][0:220], "...")