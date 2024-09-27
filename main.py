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


def search_account_by_number(element, account_number):
    results = []
    account_elements = element.xpath(f"//*[contains(text(), '{account_number}')]")
    
    for account in account_elements:
        parent = account.getparent()
        results.append({
            "AccountNumber": account.text,
            "Details": etree.tostring(parent, pretty_print=True, encoding='utf8').decode('utf8') if parent is not None else ""
    
        })
    
    return results


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
                aggregated_data.append({
                    "Name": name,
                    "Value": value,
                    "Description": description
                })

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
    st.title("User Details")

    if 'page' not in st.session_state:
        st.session_state.page = "search"

    file = './1_Account_035_Result.xml'
    root = load_xml(file)

    if root is not None and 'data' not in st.session_state:
        st.session_state.data = extract_psummary_data(root)

    if st.session_state.page == "analyze":
        analyze_page()

    elif st.session_state.page == "account_details":
        st.write(f"Results for Account Number: {st.session_state.account_number}")

        raw_data, aggregated_data = extract_data_for_account_lxml(root)

        st.write("Raw Data:")
        raw_df = pd.DataFrame(raw_data)
        if not raw_df.empty:
            st.dataframe(raw_df)
        else:
            st.write("No Raw Data Found.")

        st.write("Aggregated Data:")
        agg_df = pd.DataFrame(aggregated_data)
        if not agg_df.empty:
            st.dataframe(agg_df)
        else:
            st.write("No Aggregated Data Found.")

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

        if st.button("Back to Search", key="back_to_home_details"):
            st.session_state.page = "search"

    else:
        account_number = st.text_input("Enter Account Number to search:")

        if account_number and st.button("Search"):
            results = search_account_by_number(root, account_number)

            if results:
                st.session_state.results = results
                st.session_state.account_number = account_number
                st.session_state.page = "account_details"
            else:
                st.write(f"No results found for Account Number: {account_number}")

if __name__ == "__main__":
    main()
