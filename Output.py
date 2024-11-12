import streamlit as st
import pandas as pd
from lxml import etree
from Equifax import main1
from Experian import experian_page
from illion import illion_page


def load_xml(xml_file_path):
    try:
        tree = etree.parse(xml_file_path)
        return tree.getroot()
    except Exception as e:
        st.error(f"Error loading XML file: {e}")
        return None


# Function to extract data from the saved XML file
def extract_data_from_xml(unique_id):
    # Replace this with the correct file path where the XML file is saved from the API
    # xml_file_path = "./xyz.xml"  # Assuming the XML is saved as xyz.xml after the API call
    xml_file_path = "./1_Account_035_Result.xml" 
   
    try:
        tree = etree.parse(xml_file_path)  # Load the saved XML file
    except FileNotFoundError:
        st.error(f"File not found: {xml_file_path}")
        return None
    except Exception as e:
        st.error(f"Error parsing XML: {str(e)}")
        return None
   
    # Find the HeaderSegment for application details
    root = tree.getroot()
    
    
    # Extracting details from HeaderSegment
    header = root.find('.//HeaderSegment')
    
    applicant_id = header.get('ReferenceNumber' , '')
    country_code = header.get('Country', '')
    application_date = header.get('ApplicationDate', '')
    application_time = ""  # If you have time in a different field, adjust here
    group_member = header.get('Business', '')
    strategy_code = header.get('Product', '')
    
    # Extracting Applicant information
    applicant = root.find('.//Applicant')  # Get the first Applicant node
    
    if applicant is not None:
        first_name = applicant.get('FirstNameEN', '')
        last_name = applicant.get('LastNameEN', '')
    else:
        first_name = ''
        last_name = ''
    
    # Hardcode search type and call type as per your requirement or add conditions
    search_type = "Full Search"  # Example
    call_type = "Consumer"  # Example
    
    # Return extracted data
    return {
        "Unique ID": unique_id,
        "Application ID": applicant_id,
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



def display_output():
    st.image("logo.png", width=200)  # Logo Arrangement

    # Arrangement of the information on the page
    st.markdown(
        """
        <div class="reportview-container">
           <div class="logo-container"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Styling
    st.markdown(
        """
        <style>
            .st-emotion-cache-13ln4jf {
                max-width: 100% !important;  
                width: 100% !important;      
                padding: 4rem 1rem 10rem !important;
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
            .css-1lcbmhc {
                padding-left: 0 !important;  
                padding-right: 0 !important; 
            }
            .back-button {
                margin-left: 20%;  
            }
            .stButton {
                margin-left: 10px;  /* Adjust margin for better alignment */
            }
            .st-emotion-cache-1vt4y43 {
                display: inline-flex;
                -webkit-box-align: center;
                align-items: center;
                -webkit-box-pack: center;
                justify-content: center;
                font-weight: 400;
                padding: 0.25rem 0.75rem;
                min-height: 2.5rem;
                margin: 0px;
                line-height: 1.6;
                color: black;
                width: auto;
                user-select: none;
                border: 1px solid rgba(49, 51, 63, 0.2);
                margin-left: 100px;
            }
            .st-emotion-cache-ocqkz7 {
                display: flex;
                flex-wrap: wrap;
                -webkit-box-flex: 1;
                flex-grow: 1;
                -webkit-box-align: stretch;
                align-items: stretch;
                gap: 1rem;
                margin-left: 150px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # # # Check if the form data is available in session
    if 'unique_id' in st.session_state:
        unique_id = st.session_state.unique_id

        # Extract data for the first row from the XML
        first_row_data = extract_data_from_xml(unique_id)
        if first_row_data:
            # Fill the first row and set the next two rows with only Application ID
            data_rows = [
                {**first_row_data, "Group Member": ""}  # Include Group Member as empty
            ] + [
                {"Unique ID": unique_id, "Group Member": ""} for _ in range(2)  # Group Member is empty for all
            ]
            
            # Create a DataFrame for display
            df = pd.DataFrame(data_rows)
            df.fillna("", inplace=True)  # Replace NaN with empty string

            # Display the DataFrame in HTML table format
            st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
            # Load the appropriate content based on the selected section
            if 'page' not in st.session_state:
                st.session_state.page = None  # Set a default value
            
            if st.session_state.page == "equifax":
                main1()  # Show the Equifax data page
            elif st.session_state.page == "experian":
                experian_page()  # Show the Experian page
            elif st.session_state.page == "illion":
                illion_page()  # Show the Illion page

        # Display the table
        st.markdown(
            """
            <style>
                .dataframe {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                    border-collapse: collapse;
                    width: 85%;
                    margin-left: 100px;
                }
                .dataframe th, .dataframe td {
                    padding: 8px;
                    border-bottom: 1px solid #ddd;
                }
                .dataframe tr:hover {
                    background-color: #f5f5f5;
                }
                .navbar {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    background-color: white; /* Change to match your app's theme */
                    z-index: 1000; /* Ensure it stays on top of other elements */
                    padding: 10px; /* Optional padding */
                    border-bottom: 1px solid rgba(0, 0, 0, 0.1); /* Optional border */
                }
                /* Add spacing below header */
                .header-section {
                    padding-bottom: 20px;
                }
                .st-emotion-cache-1vt4y43 {
                    display: inline-flex;
                    -webkit-box-align: center;
                    align-items: center;
                    -webkit-box-pack: center;
                    justify-content: center;
                    font-weight: 400;
                    padding: 0.25rem 0.75rem;
                    border-radius: 0.1rem;
                    /* min-height: 1.5rem; */
                    margin: 4px;
                    line-height: 1.3;
                    color: black;
                    width: 110px;
                    user-select: none;
                    background-color: rgb(240 240 240);
                    border: 1.5px solid rgb(0 0 0);
                }
                .stButton {
                    margin-left: 110px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="navbar">', unsafe_allow_html=True)
        # Display buttons in a horizontal line below the table
        col1, col2, col3 = st.columns([1, 1, 1])  # Create 3 equal-width columns

        with col1:
            if st.button("Experian"):
                st.session_state.page = "experian"  # Navigate to Experian page
                st.rerun()
        
        with col2:
            if st.button("Equifax"):
                st.session_state.page = "equifax"  # Navigate to Equifax page
                st.rerun()
        
        with col3:
            if st.button("Illion"):
                st.session_state.page = "illion"  # Navigate to Illion page
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
         
        # Return Button to go back
        if st.button("Back"):
            if 'form_data' in st.session_state:
                del st.session_state.form_data
            st.session_state.page = "form"