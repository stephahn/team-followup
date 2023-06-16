import base64
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pyrootutils
path = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)
from copy import deepcopy
import streamlit as st
from scripts.get_data import *
from scripts.regex_matching import *
from bs4 import BeautifulSoup
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from scripts.regex_matching import DetectorPipeline

# 1. Layout


patients_id = set()
radiology_reports_id = []

@st.cache_data()
def prepare_data():
    data_retrieve = get_all_radiology_report()
    data = []
    print(len(data_retrieve["entry"]))
    for i in range(len(data_retrieve["entry"])):
        tmp_data = {"id": data_retrieve["entry"][i]["resource"]["id"],
                    "conclusion": data_retrieve["entry"][i]["resource"].get("conclusion", "No conclusion"),
                    "patient_id": data_retrieve["entry"][i]["resource"]["subject"]["reference"].split("/")[1],
                    "text": remove_html_formatting(
                        data_retrieve["entry"][i]["resource"].get("text", {}).get("div", "No text"))}
        data.append(deepcopy(tmp_data))
    return pd.DataFrame(data)
@st.cache_data()
def prepare_prefilled_data():
    ids = ['a508258761846499',
    'a411079800582267',
    'a372611551565644',
    'a956893214499959',
    'a654061970756517',
    'a857795211017352',
    'a819497684894126',
    'a819497684894128',
    'a142485449496602']
    data = []
    for id in ids:
        data_retrieve = get_one_radiology_report(id)
        tmp_data = {"id": data_retrieve["id"],
                    "conclusion": data_retrieve.get("conclusion", "No conclusion"),
                    "patient_id": data_retrieve["subject"]["reference"].split("/")[1],
                    "text": remove_html_formatting(
                        data_retrieve.get("text", {}).get("div", "No text"))}
        data.append(deepcopy(tmp_data))
    return pd.DataFrame(data)







def select_conclusion(data):
    conclusion = []
    for i in range(len(data["entry"])):
        conclusion.append(data["entry"][i]["resource"].get("conclusion", "No conclusion"))
    return conclusion

def prepare_detector_pipeline():
    detector_pipeline = DetectorPipeline()
    with open(f"{Path(__file__).parent}/detector_pipeline.yaml", "r") as f:
        detector_config = yaml.load(f, Loader=yaml.FullLoader)
    for detector in detector_config:
        detector_pipeline.add_detector(detector["regex"], detector["name"], detector["color"])
    return detector_pipeline
def add_logo():
    st.sidebar.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; margin-top: 0px; padding-top: 0">
        <h1 style="text-align: center;">RadTrack</h1>
        <img src="data:image/png;base64,{base64.b64encode(open(f"{Path(__file__).parent}/logo.png", "rb").read()).decode()}" alt="logo" width=150>
        </div>""",
                        unsafe_allow_html=True)

def remove_html_formatting(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text()
def display_data():
    #df_with_selections = datalist.copy()
    #df_with_selections.insert(0, "Select", False)
    #edited_data = st.sidebar.data_editor(df_with_selections, num_rows="dynamic",use_container_width=True,
    #                      column_order=["conclusion"], key="data_editor",
    #                            column_config={"Select": st.column_config.CheckboxColumn(required=True)},)
    #selected_indices = list(np.where(edited_data.Select)[0])
    #selected_rows = datalist[edited_data.Select]
    gb = GridOptionsBuilder.from_dataframe(st.session_state.data)
    gb.configure_selection(selection_mode="single", use_checkbox=True,pre_selected_rows=[st.session_state.sid])
    gb.configure_auto_height(autoHeight=True)
    gb.configure_column("conclusion",editable=True)
    gb.configure_pagination(paginationPageSize=25)
    gridOptions = gb.build()
    return AgGrid(st.session_state.data,
                  gridOptions=gridOptions,
                  reload_data = False,
                  update_on='GRID_CHANGED',
                  fit_columns_on_grid_load=True,
                  enable_enterprise_modules=True,
                  height=600,
                  width='100%',
                  editable=True,
                  allow_unsafe_jscode=True,
                  theme='streamlit',
                  )
def add_row():
    new_row = [[str(np.random.randint(1000000)).zfill(8), 'No conclusion', 'No patient', 'No text']]
    df_empty = pd.DataFrame(new_row, columns=st.session_state.data.columns)
    st.session_state.data = pd.concat([st.session_state.data, df_empty], axis=0, ignore_index=True)
selected_conclusion = ""
if "data" not in st.session_state:
    st.session_state["data"] = prepare_prefilled_data()
if "sid" not in st.session_state:
    st.session_state["sid"] = 0
add_logo()
add_row_button = st.button("➕ Row")
detector_pipeline = prepare_detector_pipeline()
if add_row_button:
    add_row()
selection = display_data()
selected_rows = selection['selected_rows']
if not "placeholder" in st.session_state:
    st.session_state["placeholder"] = st.empty()
if selected_conclusion!=selected_rows[0]['conclusion']:
    selected_conclusion = selected_rows[0]['conclusion']
    st.session_state["placeholder"].markdown(detector_pipeline.detect(selected_conclusion), unsafe_allow_html=True)




# detector = prepare_detector_pipeline()
#
# data = prepare_data()
# conclusions = select_conclusion(data)
# list_of_regex = st.sidebar.selectbox('Select an patient', patients_id)
#
# st.markdown(detector.detect(conclusions[9]), unsafe_allow_html=True)