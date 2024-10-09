import streamlit as st
import pandas as pd
import plotly.express as px
from lxml import etree

# Load the XML file
def load_xml(file):
    try:
        tree = etree.parse(file)
        root = tree.getroot()
        return root
    except Exception as e:
        st.error(f"Error loading XML file: {e}")
        return None


# Extract Provenir ID and Unique ID from XML file
def extract_ids_from_xml(root):
    header_segment = root.find(".//HeaderSegment")
    if header_segment is not None:
        provenir_id = header_segment.get("ProvenirID", "N/A")
        unique_id = header_segment.get("UniqueID", "N/A")
        return provenir_id, unique_id

    return "N/A", "N/A"

# Function to create analysis page
def aml_page():
    # Styling
    st.markdown(""" 
        <style>
            /* Styling for the page layout and elements */
            .st-emotion-cache-13ln4jf {
                max-width: 100% !important;
                width: 100% !important;
                padding: 4rem 1rem 10rem !important;
            }
            .dataframe {
                margin-right: 100px;
                margin-left: 100px;
            }
            .css-1lcbmhc {
                padding-left: 0 !important;
                padding-right: 0 !important;
            }
            .top-info {
                position: absolute;
                top: 10px;
                right: 10px;
                text-align: right;
                font-size: 12px;
                font-family: Arial, sans-serif;
                color: black;
            }
            .header-text {
                display: inline-block;
                vertical-align: middle;
                font-family: Arial, sans-serif;
                font-size: 20px;
                font-weight: bold;
                color: black;
            }
            .navbar {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: white;
                z-index: 1000;
                padding: 10px;
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            }
            .st-emotion-cache-165ax5l {
               width: 70% !important;
               margin-bottom: 1rem;
                color: rgb(49, 51, 63);
                border-collapse: collapse;
                border: 1px solid rgba(49, 51, 63, 0.1);
                margin-left: 180px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Load the XML file for Provenir ID and Unique ID
    file = './1_Account_035_Result.xml'
    root = load_xml(file)

    if root is None:
        st.error("Failed to load XML file.")
        return

    provenir_id, unique_id = extract_ids_from_xml(root)

    st.markdown(f"""
        <div class='top-info'>
        <b>Provenir ID:</b> {provenir_id}<br>
        <b>Unique ID:</b> {unique_id}
        </div>
    """, unsafe_allow_html=True)

    st.image("logo.png", width=200)  # Logo arrangement
    st.markdown('<div class="navbar">', unsafe_allow_html=True)
    
    # Navbar Buttons
    navbar = st.container()
    with navbar:
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

        with col1:
            if st.button("Request"):
                st.session_state.page = "Request"
        with col2:
            if st.button("Response"):
                st.session_state.page = "Response"
        with col3:
            if st.button("Demograph"):
                st.session_state.page = "Demograph"
        with col4:
            if st.button("Analyze"):
                st.session_state.page = "Analyze"
        with col5:
            if st.button("VeriCheck"):
                st.session_state.page = "VeriCheck"
        with col6:
            if st.button("AML"):
                st.session_state.page = "AML"
        with col7:
            if st.button("Fraud"):
                st.session_state.page = "Fraud"
        with col8:
            if st.button("Raw"):
                st.session_state.page = "Raw"
        with col9:
            if st.button("Aggregated"):
                st.session_state.page = "Aggregated"
        with col10:
            if st.button("Summary"):
                st.session_state.page = "Summary"

    st.markdown('</div>', unsafe_allow_html=True)

