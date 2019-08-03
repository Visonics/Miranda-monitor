import requests
import time
from datetime import datetime, timedelta
import json
from utils import date2str


class Monnit:
    # Sets up the local variables for the username/password
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.baseURL = "https://www.imonnit.com/json"
        self.token = ""

    def authentication(self):

        url = self.baseURL + "/GetAuthToken?username=" + self.username \
              + "&password=" + self.password

        response = requests.post(url)
        self.token = response.json().get("Result")

        print(url)
        print(self.token)

    def appids(self):
        poll_url = self.baseURL + "/GetApplicationID/"
        response = requests.get(poll_url)

        data = response.json().get("Result")
        print(json.dumps(data, indent=4))
        return data

    def snapshots(self):
        poll_url = self.baseURL + "/SensorList/" + self.token
        response = requests.get(poll_url)

        data = response.json().get("Result")
        print(json.dumps(data, indent=4))
        return data

    def snapshots_extended(self):
        poll_url = self.baseURL + "/SensorListExtended/" + self.token
        response = requests.get(poll_url)

        data = response.json().get("Result")
        print(json.dumps(data, indent=4))
        return data

    def sensor_data(self, sensor_id, from_date=None, to_date=None):
        if not to_date:
            to_date = date2str(datetime.utcnow())
            from_date = date2str(datetime.utcnow() - timedelta(days=7))

        poll_url = self.baseURL + "/SensorDataMessages/" + self.token + "?" +\
                   "sensorID=" + str(sensor_id) + "&fromDate=" + from_date + \
                   "&toDate=" + to_date
        response = requests.get(poll_url)
        data = None
        print(response.status_code, response.reason)
        if response.status_code == 200:
            data = response.json().get("Result")
            print(json.dumps(data, indent=4))
        return data

    def sensor_metadata(self, sensor_id, digit):

        poll_url = self.baseURL + "/SensorLookUp/" + self.token + "?" +\
                   "sensorID=" + str(sensor_id) + "&CheckDigit=" + digit
        response = requests.get(poll_url)
        data = None
        print(response.status_code, response.reason)
        if response.status_code == 200:
            data = response.json().get("Result")
            print(json.dumps(data, indent=4))
        return data

    def users(self):
        poll_url = self.baseURL + "/AccountUserList/" + self.token
        response = requests.get(poll_url)

        data = response.json().get("Result")
        print(json.dumps(data, indent=4))
        return data

    def groups(self):
        poll_url = self.baseURL + "/SensorGroupList/" + self.token
        response = requests.get(poll_url)

        data = response.json().get("Result")
        print(json.dumps(data, indent=4))
        return data

    def notifications(self, from_date=None, to_date=None):
        if not to_date:
            to_date = date2str(datetime.utcnow())
            from_date = date2str(datetime.utcnow() - timedelta(days=7))
        poll_url = self.baseURL + "/SentNotifications/" + self.token + \
                   "?from=" + from_date + "&to=" + to_date
        print(poll_url)
        response = requests.get(poll_url)

        data = response.json().get("Result")
        print(len(data), json.dumps(data, indent=4))
        return data

    def all_notifications(self):

        poll_url = self.baseURL + "/AccountNotificationList/" + self.token
        print(poll_url)
        response = requests.get(poll_url)

        data = response.json().get("Result")
        print(len(data), json.dumps(data, indent=4))
        return data

    def networks(self):
        poll_url = self.baseURL + "/NetworkList/" + self.token
        response = requests.get(poll_url)

        data = response.json().get("Result")
        print(json.dumps(data, indent=4))
        return data

    def gateways(self):
        poll_url = self.baseURL + "/GatewayList/" + self.token
        response = requests.get(poll_url)

        data = response.json().get("Result")
        print(json.dumps(data, indent=4))
        return data

    def gateway_metadata(self, gateway_id, digit):

        poll_url = self.baseURL + "/GatewayLookUp/" + self.token + "?" +\
                   "gatewayID=" + str(gateway_id) + "&CheckDigit=" + digit
        response = requests.get(poll_url)
        data = None
        print(response.status_code, response.reason)
        if response.status_code == 200:
            data = response.json().get("Result")
            print(json.dumps(data, indent=4))
        return data

    def sub_accounts(self):
        poll_url = self.baseURL + "/SubAccountList/" + self.token
        response = requests.get(poll_url)

        data = response.json().get("Result")
        print(json.dumps(data, indent=4))
        return data

    def accounts(self, account_id=None):
        query = ""
        if account_id:
            query = "?accountID=%d" % account_id
        poll_url = self.baseURL + "/AccountGet/" + self.token + query
        response = requests.get(poll_url)

        data = response.json().get("Result")
        print(json.dumps(data, indent=4))
        return data

# client
if __name__ == '__main__':
    api = Monnit("admin@mirandasolutionsgroup.com", "M0nn1tS3ns0rs")
    api.authentication()
    #data = api.snapshots()
    #print(len(data))

    #api.networks()
    #api.gateways()
    #api.sensor_data(488187)
    #api.users()
    #
    api.all_notifications()
    api.sub_accounts()
    # api.appids()
    api.sensor_metadata(488187, "SMQM")
    api.gateway_metadata(941178, "XORT")
    api.accounts(26489)
