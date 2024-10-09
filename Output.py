# import streamlit as st
# import pandas as pd
# import requests
# from lxml import etree


# def display_output():
#     st.image("logo.png", width=200)  # Logo Arrangement

#     # Arrangement of the information on the page
#     st.markdown(
#         """
#         <div class="reportview-container">
#            <div class="logo-container"></div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     # Styling
#     st.markdown(
#         """
#         <style>
#             .st-emotion-cache-13ln4jf {
#                 max-width: 100% !important;  
#                 width: 100% !important;      
#                 padding: 4rem 1rem 10rem !important;
#             }
#             .stApp {
#                 margin-left: 0rem;
#             }
#             .centered-title {
#                 text-align: center;  
#                 font-size: 40px;     
#                 font-weight: bold;   
#                 color: black;        
#             }
#             .reportview-container {
#                 background-color: black;  
#                 color: white;  
#                 height: 10px;
#                 width: 100%;
#                 margin-bottom: 30px;
#             }
#             .logo-container {
#                 display: flex;
#                 align-items: center;
#                 justify-content: center;
#             }
#             .dataframe {
#                 margin-right: 100px;
#             }
#             .css-1lcbmhc {
#                 padding-left: 0 !important;  
#                 padding-right: 0 !important; 
#             }
#             .back-button {
#                 margin-left: 20%;  
#             }
#             .stButton {
#                 margin-left: 10px;  /* Adjust margin for better alignment */
#             }
#             .st-emotion-cache-1vt4y43 {
#                 display: inline-flex;
#                 -webkit-box-align: center;
#                 align-items: center;
#                 -webkit-box-pack: center;
#                 justify-content: center;
#                 font-weight: 400;
#                 padding: 0.25rem 0.75rem;
#                 min-height: 2.5rem;
#                 margin: 0px;
#                 line-height: 1.6;
#                 color: black;
#                 width: auto;
#                 user-select: none;
#                 border: 1px solid rgba(49, 51, 63, 0.2);
#             }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

#     if 'form_data' in st.session_state:
#         form_data = st.session_state.form_data

#         # Create a DataFrame to hold the form data (with three rows for each bureau)
#         bureau_links = [
#             {'name': 'Equifax', 'link': '/pages/Equifax.py'},
#             {'name': 'Experian', 'link': '/pages/Experian.py'},
#             {'name': 'Illion', 'link': './Illion.py'}
#         ]

#         # Create a list to hold all rows of form data
#         data_rows = []
#         for bureau in bureau_links:
#             row_data = form_data.copy()  # Copy form data for each bureau
#             data_rows.append(row_data)

#         # Generate output in Table format without the "Credit Bureaus" column
#         data = pd.DataFrame(data_rows)

#         # Create columns to place buttons and table side by side
#         col1, col2 = st.columns([8, 1])  # Adjust the width ratio between the table and buttons

#         # Display the table in the first column
#         with col1:
#             st.markdown(
#                 """
#                 <style>
#                     .dataframe {
#                         border: 1px solid #ddd;
#                         padding: 8px;
#                         text-align: left;
#                         border-collapse: collapse;
#                         width: 100%;
#                     }
#                     .dataframe th, .dataframe td {
#                         padding: 8px;
#                         border-bottom: 1px solid #ddd;
#                     }
#                     .dataframe tr:hover {
#                         background-color: #f5f5f5;
#                     }
#                 </style>
#                 """,
#                 unsafe_allow_html=True
#             )
#             st.markdown(data.to_html(escape=False, index=False), unsafe_allow_html=True)

#         # Display buttons in the second column, aligned vertically
#         with col2:
#             st.markdown(
#                 """
#                 <style>
#             .stButton {
#                 display: flex;
#                 flex-direction: column;  /* Arrange buttons vertically */
#                 align-items: flex-start;  /* Align buttons to the start */
#                 gap: 10px;  /* Add space between buttons */
#                 padding-top: 10px; /* Add padding to push buttons down */
#             }
#         </style>
#                 """,
#                 unsafe_allow_html=True
#             )

#             # Buttons to navigate different pages, arranged vertically
#             if st.button("Equifax"):
#                 st.session_state.page = "data"  # Navigate to Equifax page
#                 st.rerun()
#             if st.button("Experian"):
#                 st.session_state.page = "experian"  # Navigate to Experian page
#             if st.button("Illion"):
#                 st.session_state.page = "illion"  # Navigate to Illion page

#         # Return Button to go back
#         if st.button("Return"):
#             if 'form_data' in st.session_state:
#                 del st.session_state.form_data
#             st.session_state.page = "form"


import streamlit as st
import pandas as pd
import requests
from lxml import etree

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
            # .dataframe {
            #     margin-right: 100px;
            #     margin-left: 25px;
            # }
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

    if 'form_data' in st.session_state:
        form_data = st.session_state.form_data

        # Create a DataFrame to hold the form data (with three rows for each bureau)
        bureau_links = [
            {'name': 'Equifax', 'link': '/pages/Equifax.py'},
            {'name': 'Experian', 'link': '/pages/Experian.py'},
            {'name': 'Illion', 'link': './Illion.py'}
        ]

        # Create a list to hold all rows of form data
        data_rows = []
        for bureau in bureau_links:
            row_data = form_data.copy()  # Copy form data for each bureau
            data_rows.append(row_data)

        # Generate output in Table format without the "Credit Bureaus" column
        data = pd.DataFrame(data_rows)

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
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown(data.to_html(escape=False, index=False), unsafe_allow_html=True)

        # Display buttons in a horizontal line below the table
        col1, col2, col3 = st.columns([1, 1, 1])  # Create 3 equal-width columns

        with col1:
            if st.button("Equifax"):
                st.session_state.page = "equifax"  # Navigate to Equifax page
                st.rerun()
        
        with col2:
            if st.button("Experian"):
                st.session_state.page = "experian"  # Navigate to Experian page
        
        with col3:
            if st.button("Illion"):
                st.session_state.page = "illion"  # Navigate to Illion page

        # Return Button to go back
        if st.button("Return"):
            if 'form_data' in st.session_state:
                del st.session_state.form_data
            st.session_state.page = "form"
