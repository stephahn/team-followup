from pathlib import Path

import pyrootutils
path = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)
import streamlit as st
import pandas as pd
import numpy as np
from scripts.get_data import *
from scripts.regex_matching import *

patients_id = set()
radiology_reports_id = []

st.title("Followup team")


def prepare_data():
    data = get_all_radiology_report()
    for i in range(len(data["entry"])):
        radiology_reports_id.append(data["entry"][i]["resource"]["id"])
        patients_id.add(data["entry"][i]["resource"]["subject"]["reference"].split("/")[1])
    return data

def select_conclusion(data):
    conclusion = []
    for i in range(len(data["entry"])):
        conclusion.append(data["entry"][i]["resource"].get("conclusion", "No conclusion"))
    return conclusion

def prepare_detector_pipeline():
    detector_pipeline = DetectorPipeline()
    regex = []
    with open(f"{Path(__file__).parent}/detector_pipeline.yaml", "r") as f:
        detector_config = yaml.load(f, Loader=yaml.FullLoader)
    for detector in detector_config:
        detector_pipeline.add_detector(detector["regex"], detector["name"], detector["color"])
    return detector_pipeline
detector = prepare_detector_pipeline()

data = prepare_data()
conclusions = select_conclusion(data)
list_of_regex = st.sidebar.selectbox('Select an patient', patients_id)

st.markdown(detector.detect(conclusions[9]), unsafe_allow_html=True)