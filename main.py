import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import plotly.express as px
import io

def load_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    return root

def search_account_by_number(element, account_number, parent=None):
    results = []

    if element.tag == "AccountNumber" and account_number in element.text:
        results.append({
            "Tag": parent.tag if parent is not None else element.tag,
            "Attributes": parent.attrib if parent is not None else {},
            "AccountNumber": element.text,
            "Details": ET.tostring(parent, encoding='utf8').decode('utf8') if parent is not None else ""
        })
    
    for child in element:
        results += search_account_by_number(child, account_number, element)
    
    return results

def extract_data_for_account(element):
    raw_data = []
    aggregated_data = []

    # Adjust this loop to find data under the desired tags
    for child in element.iter():
        if child.tag == "InterfaceAggregations":
            for agg_child in child.findall("InterfaceAggregationLocal/AggregationLocal"):
                # Extracting raw data if available
                for raw_item in agg_child.findall("RawData/Item"):
                    name = raw_item.find("Name").text if raw_item.find("Name") is not None else ""
                    value = raw_item.find("Value").text if raw_item.find("Value") is not None else ""
                    raw_data.append({"Name": name, "Value": value})

                # Extracting aggregated data if available
                for agg_item in agg_child.findall("AggregatedData/Item"):
                    name = agg_item.find("Name").text if agg_item.find("Name") is not None else ""
                    value = agg_item.find("Value").text if agg_item.find("Value") is not None else ""
                    description = agg_item.find("Description").text if agg_item.find("Description") is not None else ""
                    aggregated_data.append({"Name": name, "Value": value, "Description": description})

    return raw_data, aggregated_data

def analyze_page():
    st.title("Analysis Page")

    graph_type = st.selectbox("Select a graph type to display:", ["Line Graph", "Bar Graph", "Pie Chart"])

    data = pd.DataFrame({
        'Credit Name': ['Credit A', 'Credit B', 'Credit C', 'Credit D'],
        'FirstReportedLimitAmt': [10000, 15000, 5000, 20000],
        'CurrentLimit': [8000, 12000, 4500, 18000],
        'Status': ['open', 'close', 'open', 'close']
    })

    if graph_type == "Line Graph":
        st.subheader("Line Graph")
        line_fig = px.line(data, x='Credit Name', y='FirstReportedLimitAmt', title="Line Graph of FirstReportedLimitAmt")
        st.plotly_chart(line_fig)

    elif graph_type == "Bar Graph":
        st.subheader("Bar Graph")
        bar_fig = px.bar(data, x='Credit Name', y='CurrentLimit', title="Bar Graph of CurrentLimit")
        st.plotly_chart(bar_fig)

    elif graph_type == "Pie Chart":
        st.subheader("Pie Chart")
        pie_data = data['Status'].value_counts().reset_index()
        pie_data.columns = ['Status', 'Count']
        pie_fig = px.pie(pie_data, names='Status', values='Count', title="Pie Chart of Status (Open/Close)")
        st.plotly_chart(pie_fig)

    if st.button("Back"):
        st.session_state.page = "account_details"

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

    default_file = './1_Account_035_Result.xml'  
    root = load_xml(default_file)

    if st.session_state.page == "analyze":
        analyze_page()

    elif st.session_state.page == "account_details":
        st.write(f"Results for Account Number: {st.session_state.account_number}")

        raw_data, aggregated_data = extract_data_for_account(root)

        # Display raw data table
        st.write("Raw Data:")
        raw_df = pd.DataFrame(raw_data)
        if not raw_df.empty:
            st.dataframe(raw_df)
        else:
            st.write("No Raw Data Found.")

        # Display aggregated data table
        st.write("Aggregated Data:")
        agg_df = pd.DataFrame(aggregated_data)
        if not agg_df.empty:
            st.dataframe(agg_df)
        else:
            st.write("No Aggregated Data Found.")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Request"):
                request_data = "<Request><AccountNumber>{}</AccountNumber></Request>".format(st.session_state.account_number)
                download_xml_button(request_data, "request.xml")

        with col2:
            if st.button("Response"):
                response_data = ET.tostring(root, encoding='utf8').decode('utf8')
                download_xml_button(response_data, "response.xml")

        with col3:
            if st.button("Analyze"):
                st.session_state.page = "analyze"
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
