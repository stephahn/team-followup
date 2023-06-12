from dotenv import load_dotenv
load_dotenv()
import requests
import yaml
import os
import sys
import time
import datetime

url = "https://hackathon.siim.org/fhir/DiagnosticReport"

payload = {}
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'apikey': os.getenv("API_KEY")}
# 1. Load the working file

file_path = "followup_to_add.yaml"
with open(file_path, "r") as f:
    datas = yaml.safe_load(f)

for data in datas:
    data_id = data["id"]
    conclusion = data["conclusion"]
    response = requests.request("GET", f"{url}/{data_id}", headers=headers, data=payload)
    response_json = response.json()
    if "conclusion" not in response_json:
        response_json["conclusion"] = conclusion
    elif conclusion not in response_json['conclusion']:
        response_json['conclusion'] = f"{response_json['conclusion']} {conclusion}"

    response = requests.request("PUT", f"{url}/{data_id}", headers=headers, data=payload, json=response_json)
    print(response.text.encode('utf8'))