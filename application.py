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


def monnit_auth():
    api = Monnit("admin@mirandasolutionsgroup.com", "M0nn1tS3ns0rs")
    api.authentication()
    return api


def bewhere_auth():
    api = Bewhere("bwadmin@mirandasolutionsgroup.com", "Stellula2018",
                  "3y8uBuEOrS")
    api.authentication()
    return api


@app.route('/appid/monnit', methods=['GET'])
def get_monnit_appids():
    api = monnit_auth()
    readings = api.appids()
    return jsonify(readings)


@app.route('/sensor_metadata/monnit/<sensor_id>/<check_digit>', methods=['GET'])
def get_monnit_sensor_metadata(sensor_id, check_digit):
    api = monnit_auth()
    readings = api.sensor_metadata(sensor_id, check_digit)
    return jsonify(readings)


@app.route('/gateway_metadata/monnit/<sensor_id>/<check_digit>', methods=['GET'])
def get_monnit_gateway_metadata(sensor_id, check_digit):
    api = monnit_auth()
    readings = api.gateway_metadata(sensor_id, check_digit)
    return jsonify(readings)


@app.route('/sensors/monnit', methods=['GET'])
def get_monnit_snapshots():
    api = monnit_auth()
    readings = api.snapshots()
    return jsonify(readings)


@app.route('/sensors_extended/monnit', methods=['GET'])
def get_monnit_extended():
    api = monnit_auth()
    readings = api.snapshots_extended()
    return jsonify(readings)


@app.route('/sensors/monnit/<sensor_id>')
@app.route('/sensors/monnit/<sensor_id>&<from_date>&<to_date>',
           methods=['GET'])
def get_monnit_sensor(sensor_id, from_date=None, to_date=None):
    api = monnit_auth()
    readings = api.sensor_data(sensor_id, from_date, to_date)
    return jsonify(readings)


@app.route('/users/monnit', methods=['GET'])
def get_monnit_users():
    api = monnit_auth()
    readings = api.users()
    return jsonify(readings)


@app.route('/account_info/monnit/<account_id>', methods=['GET'])
def get_monnit_account_info(account_id=None):
    api = monnit_auth()
    readings = api.accounts(account_id)
    return jsonify(readings)


@app.route('/accounts/monnit', methods=['GET'])
def get_monnit_accounts():
    api = monnit_auth()
    readings = api.sub_accounts()
    return jsonify(readings)


@app.route('/gateways/monnit', methods=['GET'])
def get_monnit_gateways():
    api = monnit_auth()
    readings = api.gateways()
    return jsonify(readings)


@app.route('/networks/monnit', methods=['GET'])
def get_monnit_networks():
    api = monnit_auth()
    readings = api.networks()
    return jsonify(readings)


@app.route('/groups/monnit', methods=['GET'])
def get_monnit_groups():
    api = monnit_auth()
    readings = api.groups()
    return jsonify(readings)


@app.route('/notifications/monnit', methods=['GET'])
@app.route('/notifications/monnit/<from_date>&<to_date>',
           methods=['GET'])
def get_monnit_notifications(from_date=None, to_date=None):
    api = monnit_auth()
    readings = api.notifications(from_date, to_date)
    return jsonify(readings)


"""Bewhere API"""


@app.route('/sensors/bewhere', methods=['GET'])
def get_bewhere():
    api = bewhere_auth()
    readings = api.snapshots()
    return jsonify(readings)


@app.route('/sensors/bewhere/<sensor_id>')
@app.route('/sensors/bewhere/<sensor_id>&<from_date>&<to_date>',
           methods=['GET'])
def get_bewhere_sensor(sensor_id, from_date=None, to_date=None):
    api = bewhere_auth()
    readings = api.snapshots_id(sensor_id, from_date, to_date)
    return jsonify(readings)


@app.route('/beacons/bewhere', methods=['GET'])
def get_bewhere_beacons():
    api = bewhere_auth()
    readings = api.beacons()
    return jsonify(readings)


@app.route('/accounts/bewhere', methods=['GET'])
def get_bewhere_accounts():
    api = bewhere_auth()
    readings = api.accounts()
    return jsonify(readings)


@app.route('/users/bewhere', methods=['GET'])
def get_bewhere_users():
    api = bewhere_auth()
    readings = api.users()
    return jsonify(readings)


@app.route('/groups/bewhere', methods=['GET'])
def get_bewhere_groups():
    api = bewhere_auth()
    readings = api.groups()
    return jsonify(readings)


@app.route('/modems/bewhere', methods=['GET'])
def get_bewhere_modems():
    api = bewhere_auth()
    readings = api.modems()
    return jsonify(readings)


@app.route('/sites/bewhere', methods=['GET'])
def get_bewhere_sites():
    api = bewhere_auth()
    readings = api.sites()
    return jsonify(readings)


@app.route('/transmitters/bewhere', methods=['GET'])
def get_bewhere_transmitters():
    api = bewhere_auth()
    readings = api.transmitters()
    return jsonify(readings)


@app.route('/notifications/bewhere', methods=['GET'])
@app.route('/notifications/bewhere/<from_date>&<to_date>',
           methods=['GET'])
def get_bewhere_notifications(from_date=None, to_date=None):
    api = bewhere_auth()
    readings = api.notifications(from_date, to_date)
    return jsonify(readings)

@app.route("/")
def hello():
    return "<h1>Welome to Miranda Remote Monitoring Solution!<br>" \
           "<br>Version 0.2.3 - July 22, 2019<h1>"


if __name__ == '__main__':
    print("Starting service")
    app.run(host='0.0.0.0', port=8081, threaded=True)