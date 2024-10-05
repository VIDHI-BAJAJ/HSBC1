import streamlit as st
import pandas as pd

#main page
def display_form():
    st.image("logo.png", width=250) #Logo
    st.markdown('<h1 class="centered-title">Search Criteria</h1>', unsafe_allow_html=True) #Search Criterian
#styling 
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
        .st-emotion-cache-1vt4y43 {
        display: inline-flex;
       -webkit-box-align: center;
        align-items: center;
       -webkit-box-pack: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 10.5rem;
        min-height: 2.5rem;
         margin: 0px;
         line-height: 1.6;
        color: white !important;
         width: auto;
         user-select: none;
         background-color: rgb(23 143 255) !important;
         border: 1px solid rgba(49, 51, 63, 0.2);
        float: center;
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
    
#Arrangment of the information on the page
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
    
    #form
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

#submit info
        submitted = st.form_submit_button("Submit")
        if submitted:
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
                st.session_state.page = "output"  
            else:
                st.warning("Please enter the Application ID.")  
    #clearCriteria Info            
    if st.button("Clear Criteria"):
        for key in ['unique_id', 'application_id', 'first_name', 'last_name', 'country_code', 
                     'application_date', 'application_time', 'group_member', 'strategy_code', 
                     'search_type', 'call_type']:
            if key in st.session_state:
                del st.session_state[key]

        
        st.session_state.unique_id = "   "
        st.session_state.application_id = "   "
        st.session_state.first_name = "   "
        st.session_state.last_name = "   "
        st.session_state.country_code = "   "
        st.session_state.application_date = None
        st.session_state.application_time = None
        st.session_state.group_member = "   "
        st.session_state.strategy_code = "   "
        st.session_state.search_type = "Full Search"
        st.session_state.call_type = "Consumer"

        st.rerun()  
        
# 2nd page
def display_output():
    st.image("logo.png", width=200) #logo Arrangment
    
#Arrangment of the information on the page
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

        # Create three copies of form_data with different Credit Bureaus
        credit_bureaus = [

            '<a href="./Equifax.py" target="_blank">Equifax</a>',
            '<a href="/pages/Experian.py" target="_blank">Experian</a>',
            '<a href="./Illion.py" target="_blank">Illion</a>'
        ]

        # Generate rows with the same form data but different credit bureau links
        data_rows = []
        for bureau in credit_bureaus:
            row_data = form_data.copy()  
            row_data["Credit Bureaus"] = bureau 
            data_rows.append(row_data)

    #Generate output in Table format
        data = pd.DataFrame(data_rows)

    #Styling
        st.markdown(
            """
            <style>
             .st-emotion-cache-13ln4jf {
                max-width: 100% !important;  
                width: 100% !important;      
                padding: 4rem 1rem 10rem; !important;
            }
            .stApp {
                margin-left: 0rem;
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
                margin-left: 100px;
            }
            .css-1lcbmhc {
                padding-left: 0 !important;  
                padding-right: 0 !important; 
            }
            .back-button {
                margin-left: 20%;  
            }
            .stButton {
                margin-left: 110px;
            }
            .st-emotion-cache-1vt4y43 {
                display: inline-flex;
                -webkit-box-align: center;
                align-items: center;
                -webkit-box-pack: center;
                justify-content: center;
                font-weight: 400;
                padding: 0.25rem 0.75rem;
                border-radius: 0.5rem;
                min-height: 2.5rem;
                margin: 0px;
                line-height: 1.6;
                color: white;
                width: auto;
                user-select: none;
                background-color: rgb(22 133 238 / 99%);
                border: 1px solid rgba(49, 51, 63, 0.2);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Render the data including links in a table
        st.markdown(data.to_html(escape=False, index=False), unsafe_allow_html=True)

     #Return Button help to go Back
    if st.button("Return"):
        if 'form_data' in st.session_state:
            del st.session_state.form_data
        st.session_state.page = "form"
        
        

# Determine which page to show
if 'page' not in st.session_state:
    st.session_state.page = "form"

if st.session_state.page == "form":
    display_form()
else:
    display_output()
