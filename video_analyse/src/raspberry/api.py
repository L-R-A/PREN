import requests
import time

SERVER_URL = "https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com"
TEAM = "team01"
PASSWORD = "TOKEN_EINFÜGEN"

START_REQUEST_PATH = "/cubes/${TEAM}/start"
END_REQUEST_PATH = "/cubes/${TEAM}/end"
CONFIG_REQUEST_PATH = "/cubes/${TEAM}/config"
VALUES_REQUEST_PATH= "/cubes/${TEAM}"
PING_REQUEST_PATH= "/cubes"

AUTH = (TEAM, PASSWORD)

def ping_request():
    res = requests.get(SERVER_URL + PING_REQUEST_PATH)
    print("Response: ", res.status_code, res.text)
    
def start_request():
    print("POST/START_REQUEST: " +  SERVER_URL + START_REQUEST_PATH)
    res = requests.post(SERVER_URL + START_REQUEST_PATH, auth=AUTH)
    print("Response: ", res.status_code)

def end_request():
    print("POST/END_REQUEST: " +  SERVER_URL + END_REQUEST_PATH)
    res = requests.post(SERVER_URL + END_REQUEST_PATH, auth=AUTH)
    print("Response: ", res.status_code)

def config_request(config_in_json):
    print("POST/CONFIG_REQUEST: " +  SERVER_URL + CONFIG_REQUEST_PATH)
    res = requests.post(SERVER_URL + CONFIG_REQUEST_PATH, json=config_in_json, auth=AUTH)
    print("Response: ", res.status_code)

def values_request():
    print("GET/VALUES_REQUEST: " + SERVER_URL + VALUES_REQUEST_PATH)
    res = requests.get(SERVER_URL + VALUES_REQUEST_PATH)
    print("Response: ", res.status_code, res.text)
