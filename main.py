import streamlit as st
import xml.etree.ElementTree as ET


def load_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    return root


def search_application_by_id(root, app_id):
    results = []
    for child in root:
        
        if 'ApplicationID' in child.attrib and child.attrib['ApplicationID'] == app_id:
            results.append({
                "Tag": child.tag,
                "Attributes": child.attrib,
                "Text": child.text
            })
    return results


def main():
    st.title("XML Application ID Search")

    default_file = '1_Account_035_Result.xml'
    
    
    root = load_xml(default_file)

    app_id = st.text_input("Enter Application ID to search:")

    if app_id:
        
        results = search_application_by_id(root, app_id)
        
        if results:
            st.write(f"Results for Application ID: {app_id}")
            for result in results:
                st.json(result)  

           
            if st.button("Go to Application Details"):
           
                st.write("Redirecting to Application Details Page...")
                for result in results:
                    st.write("Application Details:")
                    st.json(result)
        else:
            st.write(f"No results found for Application ID: {app_id}")

if __name__ == "__main__":
    main()
