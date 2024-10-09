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

# #Extracting Of Raw And Aggregated data from Xml file
def extract_data_for_account_lxml(element):
    raw_data = []
    aggregated_data = []

    interface_aggregations = element.xpath(".//InterfaceAggregations")

    for interface in interface_aggregations:
        aggregation_locals = interface.xpath(".//AggregationLocal")
        for agg_local in aggregation_locals:
            raw_items = agg_local.xpath("./Raw")
            for raw_item in raw_items:
                name = raw_item.get("Name")
                value = raw_item.get("Value")
                raw_data.append({"Name": name, "Value": value})

            aggregated_items = agg_local.xpath("./Aggregated")
            for agg_item in aggregated_items:
                name = agg_item.get("Name")
                value = agg_item.get("Value")
                description = agg_item.get("Description")

                # Initialize category variable
                category = ""

                # Determine the category based on the name
                if name.startswith("G1_"):
                    category = "G1_Demographics"
                elif name.startswith("G2_"):
                    category = "G2_Age"
                elif name.startswith("G3_"):
                    category = "G3_Credit History"
                elif name.startswith("G4_"):
                    category = "G4_Employment"
                elif name.startswith("G5_"):
                    category = "G5_Financial Status"
                elif name.startswith("G6_"):
                    category = "G6_Inquiries"
                elif name.startswith("G7_"):
                    category = "G7_Public Records"
                elif name.startswith("G8_"):
                    category = "G8_Collections"
                elif name.startswith("G9_"):
                    category = "G9_Fraud"
                elif name.startswith("G10_"):
                    category = "G10_Account Details"
                else:
                    category = "Other"

                # Append to aggregated_data as a row
                aggregated_data.append([
                    category,
                    name,
                    value,
                    description,
                ])

    # Custom sorting order
    custom_category_order = {
        "G1_Demographics": 1,
        "G2_Age": 2,
        "G3_Credit History": 3,
        "G4_Employment": 4,
        "G5_Financial Status": 5,
        "G6_Inquiries": 6,
        "G7_Public Records": 7,
        "G8_Collections": 8,
        "G9_Fraud": 9,
        "G10_Account Details": 10,
        "Other": 11,
    }

    # Sort the aggregated data by category and then by Name
    aggregated_data.sort(key=lambda x: (custom_category_order.get(x[0], 11), x[1]))

    return raw_data, aggregated_data

def display_data(aggregated_data):
    current_category = None
    for entry in aggregated_data:
        category = entry["Category"]
        
        # Only print the category header if it's different from the last printed category
        if category != current_category:
            if current_category is not None:
                print()  # Add a blank line before the next category
            print(category)  # Print category header
            current_category = category
            
        # Print data entries with specific formatting
        print(f"{entry['Name']}\t{entry['Value']}\t{entry['Description']}")  # Print data entries


# Extract Provenir ID and Unique ID from XML file
def extract_ids_from_xml(root):
    header_segment = root.find(".//HeaderSegment")
    if header_segment is not None:
        provenir_id = header_segment.get("ProvenirID", "N/A")
        unique_id = header_segment.get("UniqueID", "N/A")
        return provenir_id, unique_id

    return "N/A", "N/A"


# Main function Experian
def experian_page():
    
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
    if "page_history" not in st.session_state:
        st.session_state.page_history = []

    # Navbar Buttons
    navbar = st.container()
    with navbar:
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

        with col1:
            if st.button("Request"):
               st.session_state.page_history.append(st.session_state.page)
               st.session_state.page = "Request"        
        with col2:
            if st.button("Response"):
                st.session_state.page_history.append(st.session_state.page)
                st.session_state.page = "Response"

        with col3:
            if st.button("Demograph"):
                st.session_state.page_history.append(st.session_state.page)
                st.session_state.page = "Demograph"
        with col4:
            if st.button("Analyze"):
                st.session_state.page_history.append(st.session_state.page)
                st.session_state.page = "analyze"
        with col5:
            if st.button("VeriCheck"):
                st.session_state.page_history.append(st.session_state.page)
                st.session_state.page = "VeriCheck"
        with col6:
            if st.button("AML"):
                st.session_state.page_history.append(st.session_state.page)
                st.session_state.page = "AML"
        with col7:
            if st.button("Fraud"):
                st.session_state.page_history.append(st.session_state.page)
                st.session_state.page = "Fraud"
        with col8:
            if st.button("Raw"):
                st.session_state.page_history.append(st.session_state.page)
                st.session_state.page = "Raw"
        with col9:
            if st.button("Aggregated"):
                st.session_state.page_history.append(st.session_state.page)
                st.session_state.page = "Aggregated"
        with col10:
            if st.button("Summary"):
                st.session_state.page_history.append(st.session_state.page)
                st.session_state.page = "Summary"

    st.markdown('</div>', unsafe_allow_html=True)
     
                
#Styling
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
            .dataframe {
                margin-right: 500px;
                margin-left:500px;
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

    st.title("Aggregated Data")
    # Extract raw data using the existing function
    raw_data, aggregated_data = extract_data_for_account_lxml(root)

    # Convert raw data to a DataFrame for display
    agg_df = pd.DataFrame(aggregated_data)
    if not agg_df.empty:
     st.table(agg_df)  # Display the raw data in a table format
        
         # Back button   
    if st.button("Back"):
         if len(st.session_state.page_history) > 0:
            st.session_state.page = st.session_state.page_history.pop()  # Go back to the previous page
         else:
            st.error("No previous page to go back to.")

