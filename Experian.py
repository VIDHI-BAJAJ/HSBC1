import streamlit as st
import pandas as pd
import plotly.express as px
from lxml import etree
import io


def load_xml(file):
    try:
        tree = etree.parse(file)
        root = tree.getroot()
        return root
    except Exception as e:
        st.error(f"Error loading XML file: {e}")
        return None


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

                if "Demographics" in name:
                    group = "G1 Demographics"
                elif "Age" in name:
                    group = "G2 Age"
                elif "Income" in name:
                    group = "G3 Income"
                elif "Education" in name:
                    group = "G4 Education"
                else 

                aggregated_data.append({
                    "Name": name,
                    "Value": value,
                    "Description": description,
                    "Group": group
                })

    
    aggregated_data = sorted(aggregated_data, key=lambda x: x["Name"])

    return raw_data, aggregated_data


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


def analyze_page():
    st.title("Analysis Page")
    
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.error("No data available to plot. Please check the XML file.")
        return

    data = st.session_state.data
    graph_type = st.selectbox("Select a graph type to display:", ["Line Graph", "Bar Graph", "Pie Chart"])

    if graph_type == "Line Graph":
        st.subheader("Line Graph of FirstReportedLimitAmt by Creditor Name")
        line_fig = px.line(data, x='CreditorName', y='FirstReportedLimitAmt', title="First Reported Limit Amount by Creditor Name")
        st.plotly_chart(line_fig)
    
    elif graph_type == "Bar Graph":
        st.subheader("Bar Graph of CurrentLimit by Creditor Name")
        bar_fig = px.bar(data, x='CreditorName', y='CurrentLimit', title="Current Limit by Creditor Name")
        st.plotly_chart(bar_fig)

    elif graph_type == "Pie Chart":
        st.subheader("Pie Chart of Account Status (Open vs Closed)")
        filtered_data = data[data['AccountStatus'].isin(['Open', 'Closed'])]
        if filtered_data.empty:
            st.error("No data available for Open or Closed accounts.")
            return

        pie_data = filtered_data['AccountStatus'].value_counts().reset_index()
        pie_data.columns = ['AccountStatus', 'Count']
        pie_fig = px.pie(pie_data, names='AccountStatus', values='Count', title="Distribution of Account Statuses")
        st.plotly_chart(pie_fig)
        
        if st.button("Back to Search", key="back_to_home_details"):
            st.session_state.page = "search"


def download_xml_button(xml_content, filename):
    xml_bytes = io.BytesIO()
    xml_bytes.write(xml_content.encode('utf-8'))
    xml_bytes.seek(0)
    st.download_button(
        label=f"Download {filename}",
        data=xml_bytes,
        file_name=filename,
        mime="application/xml"
    )

def main():
    st.image("logo.png", width=300)
     
    col1, col2, col3 = st.columns(3)

    with col1:
            if st.button("Request"):
                request_data = f"<Request><AccountNumber>{st.session_state.account_number}</AccountNumber></Request>"
                download_xml_button(request_data, "request.xml")

    with col2:
            if st.button("Response"):
                response_data = etree.tostring(root, pretty_print=True, encoding='utf8').decode('utf8')
                download_xml_button(response_data, "response.xml")

    with col3:
            if st.button("Analyze"):
                st.session_state.page = "analyze"



   
    st.markdown(
        """
        <style>
         .reportview-container {
                background-color: red;  
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
            padding: 4rem 1rem 10rem !important;
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

    st.markdown(
        """
        <div class="reportview-container">
           <div class="logo-container">
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )
   
    if 'page' not in st.session_state:
        st.session_state.page = "search"
    if 'account_number' not in st.session_state:
        st.session_state.account_number = ""

 
    file = './1_Account_035_Result.xml'
    root = load_xml(file)

    if root is not None and 'data' not in st.session_state:
        st.session_state.data = extract_psummary_data(root)

    if st.session_state.page == "analyze":
        analyze_page()

    else:
        st.session_state.page = "account_details"
        st.write(f"{st.session_state.account_number}")

        raw_data, aggregated_data = extract_data_for_account_lxml(root)

      
        agg_df = pd.DataFrame(aggregated_data)
        if not agg_df.empty:
            st.table(agg_df)
        else:
            st.write("No Aggregated Data Found.")

        if st.button("Back to Search", key="back_to_home_details"):
            st.session_state.page = "search"

if __name__ == "__main__":
    main()
