import streamlit as st

from explore_page import show_explore_page

from predict_page import show_predict_page

from predict_page2 import show_predict_page2

page = st.sidebar.selectbox("Explore or Interact", ("Explore", "US Imports", "Unemployment Rates"))

if page == "Explore":
    show_explore_page()
elif page == 'US Imports':
    show_predict_page()
else:
    show_predict_page2()

