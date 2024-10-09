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
    
# Extract psummary data for analysis
def extract_psummary_data(root):
    psummary_data = []
    
    for psummary in root.xpath(".//PSUMMARY"):
        creditor_name = psummary.findtext("CreditorName", default="N/A")
        first_reported_limit_amt = int(psummary.findtext("FirstReportedLimitAmt", default=0))
        current_limit = int(psummary.findtext("CurrentLimit", default=0))
        account_status = psummary.findtext("AccountStatus", default="N/A")
        credit_card_type = psummary.findtext("CreditCardType", default="N/A")
        
        psummary_data.append({
            'CreditorName': creditor_name,
            'FirstReportedLimitAmt': first_reported_limit_amt,
            'CurrentLimit': current_limit,
            'AccountStatus': account_status,
            'CreditCardType': credit_card_type  
        })
        
    return pd.DataFrame(psummary_data)

# Function to load and extract data from the uploaded XML file
def load_and_extract_data(xml_file_path):
    try:
        tree = etree.parse(xml_file_path)
        root = tree.getroot()
        data = extract_psummary_data(root)
        st.session_state.data = data
        st.success("Data successfully extracted and loaded.")
    except Exception as e:
        st.error(f"Error loading XML file: {e}")

# Extract Provenir ID and Unique ID from XML file
def extract_ids_from_xml(root):
    header_segment = root.find(".//HeaderSegment")
    if header_segment is not None:
        provenir_id = header_segment.get("ProvenirID", "N/A")
        unique_id = header_segment.get("UniqueID", "N/A")
        return provenir_id, unique_id

    return "N/A", "N/A"

# Function to create analysis page
def response_page():
    #Styling
     st.markdown(""" 
        <style>
            .st-emotion-cache-13ln4jf {
                max-width: 100% !important;
                width: 100% !important;
                padding: 4rem 1rem 10rem; !important;
            }
            .dataframe {
                margin-right: 100px;
                margin-left: 100px;
            }
            .css-1lcbmhc {
                padding-left: 0 !important;
                padding-right: 0 !important;
            }
        /* Style for the Provenir ID and Reference# */
        .top-info {
            position: absolute; 
            top: 10px; 
            right: 10px; 
            text-align: right; 
            font-size: 12px;
            font-family: Arial, sans-serif;
            color: black;
        }
       
        /* Align the text beside the logo */
        .header-text {
            display: inline-block;
            vertical-align: middle;
            font-family: Arial, sans-serif;
            font-size: 20px;
            font-weight: bold;
            color: black;
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
.st-emotion-cache-463q5x {
    margin: 0px;
    padding-right: 2.75rem;
    color: rgb(49, 51, 63);
    border-radius: 0.5rem;
    background-color: white;
}


    @media (max-width: 1024px) {
        .st-emotion-cache-1vt4y43 {
            width: 100%;  /* Make the buttons take full width on smaller screens */
            margin-bottom: 10px;  /* Add space between buttons */
        }
    }

    @media (max-width: 768px) {
        .st-emotion-cache-1vt4y43 {
            font-size: 12px;  /* Reduce the font size for smaller screens */
            padding: 0.2rem 0.6rem;  /* Reduce padding for better fit */
        }
        .st-emotion-cache-165ax5l {
    width: 90% !important;
    margin-bottom: 1rem;
    color: rgb(49, 51, 63);
    border-collapse: collapse;
    border: 1px solid rgba(49, 51, 63, 0.1);
    margin-left: 50px;
}
    }
      @media (max-width: 620px){
    .st-emotion-cache-165ax5l {
    width: 50% !important;
    margin-bottom: 1rem;
    color: rgb(49, 51, 63);
    border-collapse: collapse;
    border: 1px solid rgba(49, 51, 63, 0.1);
    margin-left: 20px;
}
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

        </style>
    """, unsafe_allow_html=True)
     # Load the XML file for Provenir_id and Unique_id
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

     st.image("logo.png", width=200) #logo Arrangment
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
                st.session_state.page = "analyze"
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
     
     st.markdown(
        """
        <style>
         .reportview-container {
                background-color: black;  
                color: white;  
                height: 5px;
                width: 100%;
                margin-bottom: 30px;
            }
            .logo-container {
                display: flex;
                align-items: center;
                justify-content: center;
            }
        .st-emotion-cache-13ln4jf {
            max-width: 100% !important;  
            width: 100% !important;      
            padding: 4rem 4rem 10rem !important;
        }
        .css-1lcbmhc {
            padding-left: 0 !important;  
            padding-right: 0 !important; 
        }
        .st-emotion-cache-165ax5l {
           width: 70% !important;
           margin-bottom: 1rem;
            color: rgb(49, 51, 63);
            border-collapse: collapse;
            border: 1px solid rgba(49, 51, 63, 0.1);
            margin-left: 180px; !important;
        }
       .st-emotion-cache-a51556 {
           border-bottom: 1px solid rgba(49, 51, 63, 0.1);
           border-right: 1px solid rgba(49, 51, 63, 0.1);
           vertical-align: middle;
           padding: 0.25rem 0.375rem;
           font-weight: 400;
           color: rgba(49, 51, 63, 0.6);
           display: none;
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
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

     file_path = './1_Account_035_Result.xml'

    # Read and display the XML content
     with open(file_path, 'r') as file:
        xml_content = file.read()

    # Create two columns for the header and download button side by side
     col1, col2 = st.columns([3, 1])

     with col1:
        st.subheader("XML File Content")
    
     with col2:
        st.download_button(
            label="Download",
            data=xml_content,
            file_name="response.xml",
            mime="application/xml"
        )

    # Display the XML content in a code block below
     st.code(xml_content, language='xml')


