import streamlit as st
import pandas as pd
from pages import student_detail
from pages.advisor_dashboard import load_data


def render(navigate_to):
    st.markdown("""
    <div class='header-container'>
        <div class='header-title'>👤 Profile</div>
        <div class='header-subtitle'>View a student profile</div>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()
    ids = df['student_id'].tolist()
    names = df['name'].tolist()
    mapping = dict(zip([f"{i} - {n}" for i,n in zip(ids,names)], ids))

    choice = st.selectbox("Select student to view profile", options=["Choose..."] + list(mapping.keys()))
    if choice and choice != "Choose...":
        sid = mapping[choice]
        navigate_to('student-detail', sid)

    st.markdown("---")
    st.markdown("<small>Select a student to open their detailed profile.</small>", unsafe_allow_html=True)
