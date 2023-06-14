import dotenv
dotenv.load_dotenv(dotenv.find_dotenv(usecwd=True))
import requests
import yaml
import os

def get_resources(endpoint, headers, params):
    url = f"https://hackathon.siim.org/fhir/{endpoint}"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload, params=params)
    return response.json()
def get_all_radiology_report():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'apikey': os.getenv("API_KEY")}
    params=None
    return get_resources("DiagnosticReport", headers, params)

def get_all_patient():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'apikey': os.getenv("API_KEY")}
    params=None
    return get_resources("Patient", headers, params)

def get_patient(patient_id):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'apikey': os.getenv("API_KEY")}
    params=None
    return get_resources(f"Patient/{patient_id}", headers, params)
