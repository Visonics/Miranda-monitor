from flask import Flask, request, jsonify, render_template
import datetime
import json
from bewhere import Bewhere
from monnit import Monnit

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
gateway_msg = None
sensor_msg = None


def read_csv(id: str):
    import csv
    fn = id + ".csv"
    messages = csv.DictReader(open(fn), delimiter=';')
    return list(messages or [])


def write_csv(data, type, id):
    import csv
    import os.path

    sensors = data.get(type, [])
    if not isinstance(sensors, list):
        sensors = [sensors]
    for sensor in sensors:
        fn = sensor[id] + ".csv"
        isFile = os.path.isfile(fn)
        print (fn, isFile)
        with open(fn, 'a', newline='') as csvfile:
            fieldnames = sensor.keys()
            writer = csv.DictWriter(csvfile, delimiter=';',
                                    fieldnames=fieldnames)

            if not isFile:
                writer.writeheader()
            writer.writerow(sensor)


@app.route('/post', methods=['POST', 'GET'])
def post():
    global gateway_msg, sensor_msg
    payload = request.json
    if 'gatewayMessage' in payload:
        gateway_msg = payload.get('gatewayMessage')
    if 'sensorMessages' in payload:    
        sensor_msg = payload.get('sensorMessages')
    write_csv(payload, 'sensorMessages', 'sensorID')
    write_csv(payload, 'gatewayMessage', 'gatewayID')        
    return jsonify(payload)


@app.route('/gateway/<gateway_id>', methods=['GET'])
def gateway(gateway_id):
    global gateway_msg, sensor_msg
    readings = read_csv(gateway_id)
    out = jsonify(readings)
    return out


@app.route('/sensors/<sensor_id>', methods=['GET'])
def sensor(sensor_id):
    global gateway_msg, sensor_msg
    readings = read_csv(sensor_id)
    print(sensor_id, readings[0])
    return jsonify(readings)


@app.route('/sensors/monnit', methods=['GET'])
def get_monnit():
    api = Monnit("admin@mirandasolutionsgroup.com", "M0nn1tS3ns0rs")
    api.authentication()
    readings = api.snapshots()
    return jsonify(readings)


@app.route('/gateways/monnit', methods=['GET'])
def get_monnit_gateways():
    api = Monnit("admin@mirandasolutionsgroup.com", "M0nn1tS3ns0rs")
    api.authentication()
    readings = api.gateways()
    return jsonify(readings)


@app.route('/sensors/bewhere', methods=['GET'])
def get_bewhere():
    api = Bewhere("bwadmin@mirandasolutionsgroup.com", "Stellula2018",
                  "3y8uBuEOrS")

    api.authentication()
    readings = api.snapshots()
    return jsonify(readings)


@app.route("/")
def hello():
    return "<h1>Welome to Miranda Remote Monitoring Solution!<br>" \
           "<br>Version 0.2.1<h1>"
