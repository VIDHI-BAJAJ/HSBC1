import streamlit as st
import pandas as pd

def display_form():
    st.image("logo.png", width=200)
    st.markdown('<h1 class="centered-title">Search Criteria</h1>', unsafe_allow_html=True)

 
    if 'unique_id' not in st.session_state:
        st.session_state.unique_id = ""
    if 'application_id' not in st.session_state:
        st.session_state.application_id = ""
    if 'first_name' not in st.session_state:
        st.session_state.first_name = ""
    if 'last_name' not in st.session_state:
        st.session_state.last_name = ""
    if 'country_code' not in st.session_state:
        st.session_state.country_code = ""
    if 'application_date' not in st.session_state:
        st.session_state.application_date = None
    if 'application_time' not in st.session_state:
        st.session_state.application_time = None
    if 'group_member' not in st.session_state:
        st.session_state.group_member = ""
    if 'strategy_code' not in st.session_state:
        st.session_state.strategy_code = ""
    if 'search_type' not in st.session_state:
        st.session_state.search_type = "Full Search"
    if 'call_type' not in st.session_state:
        st.session_state.call_type = "Consumer"

    # Define the form
    with st.form(key="search_form"):
        unique_id = st.text_input("Unique ID", value=st.session_state.unique_id)
        application_id = st.text_input("Application ID *", value=st.session_state.application_id)
        first_name = st.text_input("First Name", value=st.session_state.first_name)
        last_name = st.text_input("Last Name", value=st.session_state.last_name)
        country_code = st.text_input("Country Code", value=st.session_state.country_code)
        application_date = st.date_input("Application Date", value=st.session_state.application_date)
        application_time = st.time_input("Application Time", value=st.session_state.application_time)
        group_member = st.text_input("Group Member", value=st.session_state.group_member)
        strategy_code = st.text_input("Strategy Code", value=st.session_state.strategy_code)
        search_type = st.selectbox("Search Type", ["Full Search", "Partial Search"], index=["Full Search", "Partial Search"].index(st.session_state.search_type))
        call_type = st.selectbox("Call Type", ["Consumer", "Business"], index=["Consumer", "Business"].index(st.session_state.call_type))

        # Submit button inside the form
        submitted = st.form_submit_button("Submit")
        if submitted:
            # Only proceed if Application ID is filled
            if application_id:
                st.session_state.form_data = {
                    "Unique ID": unique_id,
                    "Application ID": application_id,
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Country Code": country_code,
                    "Application Date": application_date,
                    "Application Time": application_time,
                    "Group Member": group_member,
                    "Strategy Code": strategy_code,
                    "Search Type": search_type,
                    "Call Type": call_type,
                }
                st.session_state.page = "output"  # Navigate to the output page
            else:
                st.warning("Please enter the Application ID.")  # Show a warning if not filled

    # Add the Clear button outside the form
    if st.button("Clear Criteria"):
        # Reset the session state for all form fields
        for key in ['unique_id', 'application_id', 'first_name', 'last_name', 'country_code', 
                     'application_date', 'application_time', 'group_member', 'strategy_code', 
                     'search_type', 'call_type']:
            if key in st.session_state:
                del st.session_state[key]  # Remove key from session state

        # Reset the default values in session state
        st.session_state.unique_id = "     "
        st.session_state.application_id = "    "
        st.session_state.first_name = "    "
        st.session_state.last_name = "    "
        st.session_state.country_code = "    "
        st.session_state.application_date = None
        st.session_state.application_time = None
        st.session_state.group_member = "      "
        st.session_state.strategy_code = "    "
        st.session_state.search_type = "Full Search"
        st.session_state.call_type = "Consumer"

        st.rerun()  # Refresh to clear the form

def display_output():
    st.image("logo.png", width=200)
 
    st.markdown(
        """
        <div class="reportview-container">
           <div class="logo-container">
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if 'form_data' in st.session_state:
        form_data = st.session_state.form_data
        form_data["Credit Bureaus"] = '''
        <a href="./Equifax.py" target="_blank">Equifax</a><br>
        <a href=" http://192.168.29.25:8503" target="_blank">Experian</a><br>
        <a href="http://192.168.29.25:8504" target="_blank">Illion</a>
        '''

        data = pd.DataFrame([form_data])

        st.markdown(
            """
            <style>
            .st-emotion-cache-13ln4jf {
                max-width: 100% !important;
                width: 100% !important;      
            }
            .centered-title {
                text-align: center;  
                font-size: 40px;     
                font-weight: bold;   
                color: black;        
            }
            .reportview-container {
                background-color: black;  
                color: white;  
                height: 10px;
                width: 100%;
                margin-bottom: 30px;
            }
            .logo-container {
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .dataframe {
                margin-right: 100px;
                margin-left:100px;
            }
            .css-1lcbmhc {
                padding-left: 0 !important;  
                padding-right: 0 !important; 
            }
            .back-button {
                margin-left: 20%;  
            }
            .stButton{
                margin-left: 110px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(data.to_html(escape=False, index=False), unsafe_allow_html=True)


    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("Return"):
        if 'form_data' in st.session_state:
            del st.session_state.form_data
        st.session_state.page = "form"
    st.markdown('</div>', unsafe_allow_html=True)

# Determine which page to show
if 'page' not in st.session_state:
    st.session_state.page = "form"

if st.session_state.page == "form":
    display_form()
else:
    display_output()