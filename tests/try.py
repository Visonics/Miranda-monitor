
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

if __name__ == '__main__':
    import requests
    

    data = {
        "gatewayMessage": {
            "gatewayID": "941178",
            "gatewayName": "ChefScape-LBG-EGWY-941178",
            "accountID": "26344",
            "networkID": "57119",
            "messageType": "0",
            "power": "0",
            "batteryLevel": "101",
            "date": "2019-06-07 19:58:48",
            "count": "1",
            "signalStrength": "0",
            "pendingChange": "False"
        },
        "sensorMessages": [
            {
                "sensorID": "488187",
                "sensorName": "Chefscape freezer - 488187",
                "applicationID": "2",
                "networkID": "57119",
                "dataMessageGUID": "78851b18-80de-47be-8646-f9d171b7c62f",
                "state": "18",
                "messageDate": "2019-06-07 19:58:45",
                "rawData": "-13.3",
                "dataType": "TemperatureData",
                "dataValue": "-13.3",
                "plotValues": "8.06",
                "plotLabels": "Fahrenheit",
                "batteryLevel": "100",
                "signalStrength": "24",
                "pendingChange": "True"
            }

        ]

    }
    #res = requests.post('https://miranda-hello.azurewebsites.net/post',
    #                    json=data)
    #if res.ok:
    #    print res.json()

    write_csv(data, 'sensorMessages', 'sensorID')
    write_csv(data, 'gatewayMessage', 'gatewayID')

    print(read_csv('488187'))
