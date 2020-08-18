import pymongo
from flask import Flask, request
from bson import ObjectId
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)
client = pymongo.MongoClient(
    "mongodb://localhost:27017/test?retryWrites=true&w=majority")
db = client.flowers


@app.route('/data', methods=['GET'])
def get_data():
    fd = request.args
    if fd['to'] == "null":
        data = [item for item in db.measurements.find({'timestamp': {'$gte': int(fd['from'])}})]
    else:
        data = [item for item in db.measurements.find({'timestamp': {'$gte': int(fd['from']), '$lt': int(fd['to'])}})]
    return JSONEncoder().encode(data)


@app.route('/last_time', methods=['GET'])
def get_last_time():
    return JSONEncoder().encode(db.measurements.find().sort("timestamp", -1).limit(1)[0])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
