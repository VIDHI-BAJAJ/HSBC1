import streamlit as st
import pandas as pd

def display_form():
    st.image("logo.png", width=200)
  
    st.markdown('<h1 class="centered-title">Search Criteria</h1>', unsafe_allow_html=True)

    st.markdown(
        """
        <style>
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
        .search-label {
            font-size: 35px;  
            text-transform: uppercase;  
            margin-top: 5px;
        }
        .required {
            color: red;  
        }
        .custom-button {
            background-color: #4CAF50; 
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
            margin-right: 10px; 
        }
        .custom-button-clear {
            background-color: #f44336; 
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
        .st-emotion-cache-13ln4jf {
            max-width: 100% !important;  
            width: 100% !important;      
            padding: 4rem 1rem 10rem; !important;
        }
        .css-1lcbmhc {
            padding-left: 0 !important;  
            padding-right: 0 !important; 
        }
        .form-container {
            margin-left: 200%;  
            margin-right: 200%;  
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="reportview-container">
           <div class="logo-container">
            <div class="search-label">Search Criteria</div>
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form(key="search_form"):
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        unique_id = st.text_input("Unique ID", value="")  
        application_id = st.text_input("Application ID *", value="")  
        first_name = st.text_input("First Name", value="")
        last_name = st.text_input("Last Name", value="")
        country_code = st.text_input("Country Code", value="")
        application_date = st.date_input("Application Date", value=None)
        application_time = st.time_input("Application Time", value=None)
        group_member = st.text_input("Group Member", value="")
        strategy_code = st.text_input("Strategy Code", value="")
        search_type = st.selectbox("Search Type", ["Full Search", "Full Search","Full Search"])
        call_type = st.selectbox("Call Type", ["Consumer","Consumer","Consumer"])
        st.form_submit_button("Submit")   
        st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # with col1:
    #     if st.button("Submit"):
    #         st.session_state.form_data = {
    #             "Unique ID": unique_id,
    #             "Application ID": application_id,
    #             "First Name": first_name,
    #             "Last Name": last_name,
    #             "Country Code": country_code,
    #             "Application Date": application_date,
    #             "Application Time": application_time,
    #             "Group Member": group_member,
    #             "Strategy Code": strategy_code,
    #             "Search Type": search_type,
    #             "Call Type": call_type,
    #         }
    #         st.session_state.page = "output"

    with col2:
        if st.button("Clear Criteria"):
            for key in ['form_data', 'page']:  
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()

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


if 'page' not in st.session_state:
    st.session_state.page = "form"

if st.session_state.page == "form":
    display_form()
else:
    display_output()
