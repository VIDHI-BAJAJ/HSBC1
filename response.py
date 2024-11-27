import streamlit as st
import pandas as pd
from lxml import etree
from navigation import navigate_to, get_previous_page, get_next_page


# Load the XML file
def load_xml(file):
    try:
        tree = etree.parse(file)
        root = tree.getroot()
        return root
    except Exception as e:
        st.error(f"Error loading XML file: {e}")
        return None

# Check if XML path is in session state and load the XML file
if "xml_file_path" in st.session_state:
    xml_file_path = st.session_state.xml_file_path
    root = load_xml(xml_file_path)  # Load the XML file using the path from session state

    if root is None:
        st.error("Failed to load XML file.")
else:
    st.error("XML file path not found in session state. Please set the XML path first.")



# Extract Provenir ID and Unique ID from XML file
def extract_ids_from_xml(root):
    header_segment = root.find(".//HeaderSegment")
    if header_segment is not None:
        provenir_id = header_segment.get("ProvenirID", "N/A")
        ReferenceNumber = header_segment.get("ReferenceNumber", "N/A")
        return provenir_id, ReferenceNumber

    return "N/A", "N/A"

# Extract enquiry data and return items and requests

def extract_enquiry_data(root):
    items = [
        "Enquiry Reference Number",
        "Member Id",
        "Purpose",
        "Product",
        "Search Type",
        "Application Type",
        "Account Type",
        "Amount",
        "Terms",
        "ClientReference1",
        "ClientReference2",
        "Credit Purpose",
        "ConsUIQVersion",
        "ConsUOFVersion"
    ]


    requests = []
    for enquiry in root.xpath('.//PENQUIRY'):
     requests.append([
        enquiry.xpath('ClientEnquiryRefNumber/text()')[0] if enquiry.xpath('ClientEnquiryRefNumber/text()') else " ",
        enquiry.xpath('EnqBureauMemberId/text()')[0] if enquiry.xpath('EnqBureauMemberId/text()') else " ",
        enquiry.xpath('EnqPurpose/text()')[0] if enquiry.xpath('EnqPurpose/text()') else " ",
        enquiry.xpath('EnqProduct/text()')[0] if enquiry.xpath('EnqProduct/text()') else " ",
        enquiry.xpath('Product/text()')[0] if enquiry.xpath('Product/text()') else " ",
        enquiry.xpath('EnquiryApplicationType/text()')[0] if enquiry.xpath('EnquiryApplicationType/text()') else " ",
        enquiry.xpath('EnquiryAccountType/text()')[0] if enquiry.xpath('EnquiryAccountType/text()') else " ",
        enquiry.xpath('EnquiryAmount/text()')[0] if enquiry.xpath('EnquiryAmount/text()') else " ",
        enquiry.xpath('EnquiryTerms/text()')[0] if enquiry.xpath('EnquiryTerms/text()') else " ",
        enquiry.xpath('ClientReference1/text()')[0] if enquiry.xpath('ClientReference1/text()') else " ",
        enquiry.xpath('ClientReference2/text()')[0] if enquiry.xpath('ClientReference2/text()') else " ",
        enquiry.xpath('EnquiryCreditPurpose/text()')[0] if enquiry.xpath('EnquiryCreditPurpose/text()') else " ",
        root.xpath('.//ENQHEADER/ConsUIQVersion/text()')[0] if root.xpath('.//ENQHEADER/ConsUIQVersion/text()') else " ",  # Use root to access ENQHEADER
        root.xpath('.//ENQHEADER/ConsUOFVersion/text()')[0] if root.xpath('.//ENQHEADER/ConsUOFVersion/text()') else " ",  # Use root to access ENQHEADER
    ])

    
    return items, requests


def extract_summary_data(root):
    item = [
        "systemMessageCode",
        "systemMessageText",
        "systemMessageDescription",
    ]
    
    response = []
    for enquiry in root.xpath('.//SYSMESSG'):
        response.append([
            enquiry.xpath('systemMessageCode/text()')[0] if enquiry.xpath('systemMessageCode/text()') else " ",
            enquiry.xpath('systemMessageText/text()')[0] if enquiry.xpath('systemMessageText/text()') else " ",
            enquiry.xpath('systemMessageDescription/text()')[0] if enquiry.xpath('systemMessageDescription/text()') else " ",
        ])

    return item , response, 
    
    
# Function to create Response page
def response_page():
    #Styling
     st.markdown(""" 
        <style>
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
     
  
     provenir_id, ReferenceNumber = extract_ids_from_xml(root)


     st.markdown(f"""
        <div class='top-info'>
        <b>Provenir ID:</b> {provenir_id}<br>
        <b>Reference:</b> {ReferenceNumber}
        </div>
    """, unsafe_allow_html=True)

     st.image("logo.png", width=200) #logo Arrangment
     st.markdown('<div class="navbar">', unsafe_allow_html=True)
    # Navbar Buttons
     if "page_history" not in st.session_state:
        st.session_state.page_history = []

    # Navbar Buttons
     navbar = st.container()
     with navbar:
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([1,1,1,1,1,1,1,1,1,1])

        with col1:
            if st.button("Request", key="request_btn"):
                navigate_to("request") 

                 
        with col2:
            if st.button("Response", key="response_btn"):
               navigate_to("response")
               
        with col3:
            if st.button("Demograph", key="demograph_btn"):
                navigate_to("demograph") 
                       
        with col4:
            if st.button("Analyze", key="analyze_btn"):
                navigate_to("analyze")
                       
        with col5:
            if st.button("VeriCheck", key="vericheck_btn"):
                navigate_to("vericheck")
                
        with col6:
            if st.button("AML", key="aml_btn"):
                navigate_to("aml")
                
        with col7:
            if st.button("Fraud", key="fraud_btn"):
                navigate_to("fraud")
                
        with col8:
            if st.button("Raw", key="raw_btn"):
               navigate_to("raw")
               
        with col9:
            if st.button("Aggregated", key="aggregated_btn"):
                navigate_to("aggregated")
                  
        with col10:
            if st.button("Summary", key="summary_btn"):
                navigate_to("summary")

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
        .st-emotion-cache-1fy0zab {
         font-size: 1rem;
         line-height: 1.5;
         overflow: overlay;
         margin-left: -40px;
        }
        .st-emotion-cache-165ax5l {
           width: 70% !important;
           margin-bottom: 1rem;
            color: rgb(49, 51, 63);
            border-collapse: collapse;
            border: 1px solid rgba(49, 51, 63);
            margin-left: 180px; !important;
        }
       .st-emotion-cache-a51556 {
           border-bottom: 1px solid rgba(49, 51, 63);
           border-right: 1px solid rgba(49, 51, 63);
           vertical-align: middle;
           padding: 0.25rem 0.375rem;
           font-weight: 400;
           color: rgba(49, 51, 63);
        }
        .st-emotion-cache-a51556 {
    border-bottom: 1px solid rgb(49 ,51 ,63);
    border-right: 1px solid rgb(49 ,51 ,63);
    vertical-align: middle;
    padding: 0.25rem 0.375rem;
    font-weight: 400;
    color: rgba(49, 51, 63);
    background-color: lightgray;
}
    .st-emotion-cache-gdzsw5 {
       border-bottom: 1px solid rgb(49 ,51 ,63);
       border-right: 1px solid rgb(49 ,51 ,63);
       vertical-align: middle;
       padding: 0.25rem 0.375rem;
    font-weight: 400;
}
.st-emotion-cache-gdzsw5 {
    border-bottom: 1px solid rgba(49, 51, 63);
    border-right: 1px solid rgb(49 ,51 ,63);
    vertical-align: middle;
    padding: 0.25rem 0.375rem;
    font-weight: 400;
}
 .st-emotion-cache-165ax5l {
             width: 50% !important;
             margin-bottom: 1rem;
             color: rgb(49, 51, 63);
             border-collapse: collapse;
             border: 1px solid rgb(49 ,51 ,63);
             margin-left: 50px;
             margin-top: 20px;
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

 # Extract enquiry data
     items, requests = extract_enquiry_data(root)

    # Create DataFrame for the table
     if requests:
      request_data = requests[0]  # Get the first request data only
    
    # Create a DataFrame with items as index and corresponding values
     data = {
        'Item': items,
        'Request': request_data
    }
    
   
    # Create DataFrame for the table
     if requests:
      request_data = requests[0]  # Get the first request data only
    
    # Create a DataFrame with items as index and corresponding values
     data = {
        'Item': items,
        'Request': request_data
    }
    
    # Convert to DataFrame
     requests_df = pd.DataFrame(data)

    # Display the table
     st.table(requests_df)
     
     item, response = extract_summary_data(root)

    # Create DataFrame for the table
     if response:
      response_data = response[0]  # Get the first request data only
    
    # Create a DataFrame with items as index and corresponding values
     data = {
        'Item': item,
        'Response': response_data
    }
    

    # Convert to DataFrame
     response_df = pd.DataFrame(data)

    # Display the table
     st.table(response_df)

    # Optionally, create a DataFrame for download
     if requests:
        csv_data = requests_df.to_csv(index=False)
        
   # Adding custom CSS styling for buttons
     st.markdown("""
    <style>
        /* Style for the Back button */
        .stButton button {
            background-color: rgb(240, 240, 240);
            border: 1.5px solid rgb(0, 0, 0);
            padding: 0.25rem 0.75rem;
            font-weight: 400;
            color: black;
            cursor: pointer;
            text-align: center;
        }

        /* Style for the Download button */
        .stDownloadButton button {
            position: absolute;
            top: -740px;
            right: 20px;  /* Adjust margin as needed */
            background-color: rgb(240, 240, 240);
            border: 1.5px solid rgb(0, 0, 0);
            padding: 0.25rem 0.75rem;
            font-weight: 400;
            color: black;
            cursor: pointer;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Create two columns for "Back" and "Download" buttons
     col1, col2 = st.columns([1, 1])  # Equal width columns

# Back button
     with col1:
      if st.button("Back"):
        prev_page = get_previous_page(st.session_state.page)
        navigate_to(prev_page)

# Download button moved to top right side
     with col2:
    # Get the XML file content dynamically using the file path stored in session state
      if "xml_file_path" in st.session_state:
        xml_file_path = st.session_state.xml_file_path
        with open(xml_file_path, "rb") as file:
            xml_data = file.read()  # Read the binary data from the XML file

        st.download_button(
            label="Download",
            data=xml_data,
            file_name=xml_file_path.split("/")[-1],  # Extract the file name dynamically
            mime='application/xml'
        )