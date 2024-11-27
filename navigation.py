import streamlit as st

def get_page_sequence():
    return [
        "form",
        "output",
        "equifax",
        "experian",
        "illion",
        "analyze",
        "response",
        "request",
        "demograph",
        "vericheck",
        "aml",
        "fraud",
        "summary",
        "raw",
        "aggregated"
    ]

def get_next_page(current_page):
    sequence = get_page_sequence()
    current_index = sequence.index(current_page)
    if current_index < len(sequence) - 1:
        return sequence[current_index + 1]
    return current_page

def get_previous_page(current_page):
    sequence = get_page_sequence()
    current_index = sequence.index(current_page)
    if current_index > 0:
        return sequence[current_index - 1]
    return current_page

def navigate_to(page):
    st.query_params["page"] = page
    st.session_state.page = page
    st.rerun()