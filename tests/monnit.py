import hashlib
import requests
import time
import json


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

    def snapshots(self):
        poll_url = self.baseURL + "/SensorList/" + self.token
        response = requests.get(poll_url)

        # print(response.text)
        data = response.json().get("Result")
        print(len(data))
        print(json.dumps(data, indent=4))

    def beacons(self):
        poll_url = self.baseURL + "/accounts/" + self.accountKey + "/beacons"
        response = requests.get(poll_url, headers=self.headers)

        print(response.text)

    def beacon(self, deviceId):
        print("beacon: %s" % deviceId)

    def setConfig(self, deviceId):
        postUrl = self.baseURL + "/accounts/" + self.accountKey + \
                  "/beacons/configuration/" + deviceId
        # print postUrl

        # timer config
        """
        data = {"deviceMode":1,
            "workingMode":0,
            "sensor":0,
            "interval":300,
            "interruptConfig":{"inner":0,"outter":0,"actThresh":0,"actTime":0,
            "inactThresh":0,"inactTime":0}}
        """

        """
        #motion sample
        data = {"deviceMode":1,
            "workingMode":1,
            "sensor":1,
            "interval":60,
            "interruptConfig":{"inner":3,"outter":360,"actThresh":150,
            "actTime":10,"inactThresh":150,"inactTime":10}}
    
        #motion start/stop sample
        data = {"deviceMode":1,
            "workingMode":3,
            "sensor":1,
            "interval":60,
            "interruptConfig":{"inner":3,"outter":72,"actThresh":300,"actTime":32,"inactThresh":256,"inactTime":64}}
    
        """

        # motion sample
        data = {"deviceMode": 1,
                "workingMode": 1,
                "sensor": 1,
                "interval": 120,
                "interruptConfig": {"inner": 3, "outter": 90, "actThresh": 150,
                                    "actTime": 16, "inactThresh": 128,
                                    "inactTime": 32}}

        response = requests.post(postUrl, json=data, headers=self.headers)
        print(response.text)

    def getConfig(self, deviceId):
        # postUrl = "https://api.bewhere.com/accounts/OAgpNv7FNE/beacons/configuration/357591080070896"
        postUrl = self.baseURL + "/accounts/" + self.accountKey + \
                  "/beacons/configuration/" + deviceId
        print(postUrl)
        response = requests.get(postUrl, headers=self.headers)
        print(response.json())

    def pollHistory(self, watermark):
        self.maxDate = watermark

        if self.maxDate == 0:
            self.maxDate = (time.time() - 60 * 5) * 1000

        query = "&start=%d&end=%d" % (self.maxDate, time.time() * 1000)
        url = self.baseURL + "/accounts/" + self.accountKey + \
            "/streams/history?limit=100%s" % query
        print("Request:  %s" % url)
        # logger.log("Request:  %s" % url)

        historyData = requests.get(url, headers=self.headers)
        # print historyData.text
        data = historyData.json()

        self.maxDate = long(data["maxDate"])

    def getBeaconFota(self, deviceId):
        url = self.baseURL + "/accounts/" + self.accountKey + "/fota/%s" % deviceId
        print("Request:  %s" % url)

        response = requests.get(url, headers=self.headers)
        print(response.json())


# clients

# api = Bewhere(<username>, <password>, <accountId>)
api = Monnit("admin@mirandasolutionsgroup.com", "M0nn1tS3ns0rs")

api.authentication()
# api.beacon("357591080419283")
# api.beacons()
api.snapshots()
# api.pollHistory(1530736802332)
# api.configuration("357591080419283")
