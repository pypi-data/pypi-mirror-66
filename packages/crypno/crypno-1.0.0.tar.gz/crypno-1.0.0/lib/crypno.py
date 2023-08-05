import requests
import json

class Crypno:
    # Class Construct
    # Get Api Key : Required
    def __init__(self, apiKey):
        self.apiKey = apiKey

	# send request to api
    def request_api(self, opts):
        headers = {
            'Accept': "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            'charset': "utf-8",
            'apiKey': self.apiKey
        }

        url = 'https://crypno.ir/api/licenses/' + opts['path']

        data = opts['data']

        r = requests.post(url, data=data, headers=headers)

        return r

    # Get All Licenses
    def getAllLicenses(self):
        data = {}
        data['path'] = ""
        data['data'] = {}
        r = self.request_api(data)
        if r.status_code == 200: 
            return r.content.decode()
        return r


    # Generate New License
    def generateNewLicense(self, options):
        data = {}
        data['path'] = "generate"
        data['data'] = {
            'type' : options['type'],
            'product' : options['product'],
        }
        if "expiry_date" in options:
            data['data']['expiry_date'] = options['expiry_date']

        r = self.request_api(data)
        return r.content.decode()


    # Submit New Client
    def submitNewClient(self, options):
        data = {}
        data['path'] = "submit"
        data['data'] = {
            'license_code' : options['license_code'],
        }
        if "custom_validation_option" in options:
            data['data']['custom_validation_option'] = options['custom_validation_option']

        r = self.request_api(data)
        return r.content.decode()


    # Check A License By IP
    def checkByIP(self, license_code):
        data = {}
        data['path'] = "checkByIP"
        data['data'] = {
            'license_code' : license_code
        }
        r = self.request_api(data)
        return r.content.decode()


    # Check A License By Custom Validation Option
    def checkByCustomValidation(self, options):
        data = {}
        data['path'] = "checkByCustomValidation"
        data['data'] = {
            'license_code' : options['license_code'],
            'custom_validation_option' : options['custom_validation_option'],
        }
        r = self.request_api(data)
        return r.content.decode()