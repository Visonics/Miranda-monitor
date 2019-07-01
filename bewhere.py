import hashlib
import requests
import time
import json


class Bewhere:
    ## Sets up the local variables for the username/password
    def __init__(self, username, password, key):
        self.username = username
        self.password = password
        self.accountKey = key

        self.baseURL = "https://api.bewhere.com"
        self.token = ""

    def authentication(self):

        url = self.baseURL + "/authentication/" + self.username \
              + "?type=m2m&ttl=1"

        # Set the standard headers to include the token
        self.headers = {'Token': self.token,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                        }

        if self.token == "":
            response = requests.get(url)
            response_data = response.json()

            hashGen = hashlib.sha256()

            # Hash our password
            a = bytearray()
            # encode the password hashgen request for encoded data
            a.extend(self.password.encode())
            hashGen.update(a)
            first_hash = hashGen.hexdigest()

            # Add it to the salt
            b = bytearray()
            concat = response_data["salt"] + first_hash
            b.extend(concat.encode())
            hashGen_final = hashlib.sha256()
            hashGen_final.update(b)
            final_hash = hashGen_final.hexdigest()

            self.token = response_data["token"]

            # Post data to send back
            data = {'authphrase': final_hash,
                    'username': self.username,
                    'tidHashAlgorithm': '2',
                    'tidSession': '3'}

            # Set the standard headers to include the token
            self.headers = {'Token': self.token,
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                            }

            post_url = self.baseURL + "/authentication"
            response = requests.post(post_url, json=data, headers=self.headers)

            print(post_url)
            # print(response.text)
            print(json.dumps(response.json(), indent=4))

    def snapshots(self):
        poll_url = self.baseURL + "/accounts/" + self.accountKey + "/snapshots"
        response = requests.get(poll_url, headers=self.headers)

        # print(response.text)
        data = response.json()
        print(json.dumps(data, indent=4))
        return data

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


# client
if __name__ == '__main__':
    # api = Bewhere(<username>, <password>, <accountId>)
    api = Bewhere("bwadmin@mirandasolutionsgroup.com", "Stellula2018",
                  "3y8uBuEOrS")

    api.authentication()
    data = api.snapshots()
    print(len(data))
    # api.beacon("357591080419283")
    # api.beacons()

    # api.pollHistory(1530736802332)
    # api.configuration("357591080419283")
