import requests
import rasp_helper as hp

SERVER_URL = "https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com"
TEAM = "team01"
AUTH = "UxAVsRdu6n7A"

START_REQUEST_PATH = f"/cubes/{TEAM}/start"
END_REQUEST_PATH = f"/cubes/{TEAM}/end"
CONFIG_REQUEST_PATH = f"/cubes/{TEAM}/config"
VALUES_REQUEST_PATH= f"/cubes/{TEAM}"
PING_REQUEST_PATH= "/cubes"

class REST: 
    def ping_request():
        res = requests.get(SERVER_URL + PING_REQUEST_PATH)
        print("Response: ", res.status_code, res.text, "\n")
        
    def start_request():
        print("POST/START_REQUEST: " +  SERVER_URL + START_REQUEST_PATH)
        res = requests.post(SERVER_URL + START_REQUEST_PATH, headers={'Auth': AUTH})
        print("Response: ", res.status_code, "\n")

    def end_request():
        print("POST/END_REQUEST: " +  SERVER_URL + END_REQUEST_PATH)
        res = requests.post(SERVER_URL + END_REQUEST_PATH, headers={'Auth': AUTH})
        print("Response: ", res.status_code, "\n")

    def config_request(config_as_list):
        config_as_json = hp.JSON.convert_numpy_to_json(config_as_list)

        print("POST/CONFIG_REQUEST: " +  SERVER_URL + CONFIG_REQUEST_PATH)
        print("JSON CONFIG: ")
        print(config_as_json) # 'time' is converted to UTC --> REST-API also responds in UTC and not our timezone

        res = requests.post(SERVER_URL + CONFIG_REQUEST_PATH, data=config_as_json, headers={'Auth': AUTH, 'Content-Type': 'application/json'})
        print("Response: ", res.status_code, "\n")

    def values_request():
        print("GET/VALUES_REQUEST: " + SERVER_URL + VALUES_REQUEST_PATH)
        res = requests.get(SERVER_URL + VALUES_REQUEST_PATH)
        print("Response: ", res.status_code, res.text, "\n")

# EXAMPLE OF USAGE
# REST.start_request()
# REST.config_request(['red', 'blue', 'red', 'red', 'blue', 'yellow', '', ''])
# REST.end_request()
# REST.values_request()
