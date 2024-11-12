import streamlit as st
from mains import display_form  # Import the form page function
from Output import display_output  # Import the output page function
from Equifax import main1  # Assuming main1 is the correct function name for the data page
from Experian import experian_page  # Assuming main1 is the correct function name for the data page
from illion import illion_page  # Assuming main1 is the correct function name for the data page
from analyze import analyze_page # Assuming analyse_page is the correct function name for the anlayze page
from response import response_page # Assuming response_page is the correct function name for the response page
from request import request_page # Assuming request_page is the correct function name for the request page
from raw import raw_page # Assuming raw_page is the correct function name for the raw page
from summary import summary_page # Assuming summary_page is the correct function name for the summary page
from aggregated import aggregated_page # Assuming aggregated_page is the correct function name for the aggregated page
from demograph import demograph_page # Assuming aggregated_page is the correct function name for the aggregated page
from vericheck import vericheck_page # Assuming aggregated_page is the correct function name for the aggregated page
from fraud import fraud_page # Assuming aggregated_page is the correct function name for the aggregated page
from aml import aml_page # Assuming aggregated_page is the correct function name for the aggregated page

# Main logic for navigation
def main():
    # If there is no 'page' in session state, start on the form page
    if 'page' not in st.session_state:
        st.session_state.page = "form"  # Default to form page
    

    # Navigation control
    if st.session_state.page == "form":
       display_form()  # Show the form page
    elif st.session_state.page == "output":
       display_output()  # Show the output page
    elif st.session_state.page == "equifax":
       main1()  # Show the data page
    elif st.session_state.page == "experian":
       experian_page()# show the experian page
    elif st.session_state.page == "illion":
       illion_page() #show the illion page
    elif st.session_state.page == "analyze":
       analyze_page() #show the analyze page
    elif st.session_state.page == "Response":
       response_page() #show the response page
    elif st.session_state.page == "Request":
       request_page() #show the request page
    elif st.session_state.page == "Demograph":
        demograph_page() # show the demograph
    elif st.session_state.page == "VeriCheck":
        vericheck_page() # show the vericheck page
    elif st.session_state.page == "AML":
        aml_page() # show the aml page
    elif st.session_state.page == "Fraud":
        fraud_page() #show the fraud page
    elif st.session_state.page == "Summary":
        summary_page()  #show the summary page 
    elif st.session_state.page == "Raw":
        raw_page() #show the raw page
    elif st.session_state.page == "Aggregated":
        aggregated_page() #show the aggreagted

if __name__ == "__main__":  # Corrected the name check
    main()  # Call the main function to run the app