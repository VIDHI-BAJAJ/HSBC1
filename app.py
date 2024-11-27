# app.py
import streamlit as st
from mains import display_form
from Output import display_output
from Equifax import main1
from Experian import experian_page
from illion import illion_page
from analyze import analyze_page
from response import response_page
from request import request_page
from raw import raw_page
from summary import summary_page
from aggregated import aggregated_page
from demograph import demograph_page
from vericheck import vericheck_page
from fraud import fraud_page
from aml import aml_page

def app():
    # Get the current page from URL parameter
    current_page = st.query_params.get("page", "form")
    
    # Update session state based on URL
    if 'page' not in st.session_state or st.session_state.page != current_page:
        st.session_state.page = current_page
    
    # Navigation control
    pages = {
        "form": display_form,
        "output": display_output,
        "equifax": main1,
        "experian": experian_page,
        "illion": illion_page,
        "analyze": analyze_page,
        "response": response_page,
        "request": request_page,
        "demograph": demograph_page,
        "vericheck": vericheck_page,
        "aml": aml_page,
        "fraud": fraud_page,
        "summary": summary_page,
        "raw": raw_page,
        "aggregated": aggregated_page
    }
    
    if current_page in pages:
        pages[current_page]()

if __name__ == "__main__":
    app()

